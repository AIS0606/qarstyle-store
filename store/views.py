from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from .models import Product, Category, Favorite, Department, Size, Color, ProductVariant, ProductImage

def _attach_card_colors(products):
    """Attach a list of distinct Color objects with image URL info to each product for card swatches."""
    for product in products:
        # Get all images for this product that have a color
        color_images = {}
        for img in product.images.all():
            if img.color_id and img.image:
                color_images[img.color_id] = img.image.url
        
        # Original color has the main product image
        if product.original_color_id and product.image:
            color_images[product.original_color_id] = product.image.url
            
        # Collect distinct color IDs from variants and images
        variant_color_ids = set()
        for v in product.variants.all():
            if v.color_id:
                variant_color_ids.add(v.color_id)
        image_color_ids = set(color_images.keys())
        all_ids = variant_color_ids | image_color_ids
        
        # Query the Colors
        colors = Color.objects.filter(pk__in=all_ids)
        
        card_colors_data = []
        for c in colors:
            img_url = color_images.get(c.id)
            if not img_url and product.image:
                img_url = product.image.url
            card_colors_data.append({
                'id': c.id,
                'name': c.name,
                'hex_code': c.hex_code or '#888',
                'image_url': img_url or '',
                'is_original': c.id == product.original_color_id
            })
            
        # Ensure the original color is included at the start if not present
        has_original = any(x['is_original'] for x in card_colors_data)
        if not has_original:
            if product.original_color:
                card_colors_data.insert(0, {
                    'id': product.original_color.id,
                    'name': product.original_color.name,
                    'hex_code': product.original_color.hex_code or '#888',
                    'image_url': product.image.url if product.image else '',
                    'is_original': True
                })
            else:
                card_colors_data.insert(0, {
                    'id': 'original',
                    'name': 'Оригинал',
                    'hex_code': '#1a1a1a',
                    'image_url': product.image.url if product.image else '',
                    'is_original': True
                })
            
        product.card_colors = card_colors_data
    return products

def index(request):
    from .models import Block
    if request.user.is_staff and request.GET.get('preview') == 'true':
        blocks = Block.objects.all().prefetch_related('items').order_by('order')
    else:
        blocks = Block.objects.filter(is_active=True).prefetch_related('items').order_by('order')
    
    products = list(Product.objects.filter(available=True).select_related('original_color').prefetch_related('variants__color', 'images__color')[:4])
    _attach_card_colors(products)
    favorite_ids = get_favorite_ids(request)
    return render(request, 'store/index.html', {
        'products': products,
        'favorite_ids': favorite_ids,
        'blocks': blocks
    })

def catalog(request):
    categories = Category.objects.all()
    departments = Department.objects.all()
    # Only show sizes that have at least one variant with stock > 0
    sizes = Size.objects.filter(variants__stock__gt=0).distinct().order_by('name')
    products = Product.objects.filter(available=True).select_related('original_color').prefetch_related('variants__color', 'images__color')
    
    # Логика поиска
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)
        
    # Логика фильтрации по отделу
    department_slug = request.GET.get('department')
    if department_slug:
        products = products.filter(department__slug=department_slug)
        
    # Спец. фильтры: распродажа и перепродажа
    if request.GET.get('sale') == '1':
        products = products.filter(is_sale=True)
    if request.GET.get('resale') == '1':
        products = products.filter(is_resale=True)
    
    # Логика фильтрации по категориям
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    # Логика фильтрации по размерам (через ProductVariant)
    selected_sizes = request.GET.getlist('size')
    if selected_sizes:
        products = products.filter(variants__size__id__in=selected_sizes, variants__stock__gt=0).distinct()
        
    favorite_ids = get_favorite_ids(request)
    products_list = list(products)
    _attach_card_colors(products_list)
    return render(request, 'store/catalog.html', {
        'products': products_list,
        'categories': categories,
        'departments': departments,
        'sizes': sizes,
        'selected_categories': [int(i) for i in selected_categories if i.isdigit()],
        'selected_sizes': [int(i) for i in selected_sizes if i.isdigit()],
        'selected_department': department_slug,
        'selected_sale': request.GET.get('sale') == '1',
        'selected_resale': request.GET.get('resale') == '1',
        'search_query': search_query or '',
        'favorite_ids': favorite_ids
    })

def about(request):
    return render(request, 'store/about.html')

def product_detail(request, product_id):
    from .models import ProductImage, Color, ProductVariant
    import json as _json

    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(available=True).exclude(id=product_id).order_by('?')[:4]
    favorite_ids = get_favorite_ids(request)

    recommended_size = None
    if request.user.is_authenticated:
        try:
            body_profile = request.user.body_profile
            dept_slug = product.department.slug if product.department else None
            recommended_size = body_profile.get_recommended_size(dept_slug)
        except Exception:
            pass

    # Collect distinct non-null colors: from variants OR color-specific images
    variant_color_ids = set(product.variants.filter(color__isnull=False).values_list('color_id', flat=True))
    image_color_ids  = set(ProductImage.objects.filter(product=product, color__isnull=False).values_list('color_id', flat=True))
    all_color_ids = variant_color_ids | image_color_ids
    product_colors = list(Color.objects.filter(pk__in=all_color_ids))

    # Build color_images_json: {color_id: [url1, url2, ...]} for JS switcher
    color_images_json = {}
    for color in product_colors:
        urls = list(ProductImage.objects.filter(product=product, color=color).values_list('image', flat=True))
        color_images_json[str(color.id)] = [f'/media/{u}' for u in urls]

    # Extra images (no color) for fallback
    extra_image_urls = list(ProductImage.objects.filter(product=product, color__isnull=True).values_list('image', flat=True))
    extra_image_urls = [f'/media/{u}' for u in extra_image_urls]

    # Size availability per color (for JS)
    size_data = {}
    for color in product_colors:
        size_data[str(color.id)] = [
            {'name': v.size.name, 'stock': v.stock}
            for v in product.variants.filter(color=color).select_related('size').order_by('size__name')
        ]
    # Base sizes (no color)
    base_sizes = [
        {'name': v.size.name, 'stock': v.stock}
        for v in product.variants.filter(color__isnull=True).select_related('size').order_by('size__name')
    ]

    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'favorite_ids': favorite_ids,
        'is_favorite': product.id in favorite_ids,
        'product_colors': product_colors,
        'color_images_json': _json.dumps(color_images_json),
        'extra_image_urls': _json.dumps(extra_image_urls),
        'size_data_json': _json.dumps(size_data),
        'base_sizes_json': _json.dumps(base_sizes),
        'recommended_size': recommended_size,
    })

def get_cart_data(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = 0
    for cart_key, item_data in cart.items():
        item_total = item_data['price'] * item_data['quantity']
        subtotal += item_total
        cart_items.append({
            'cart_key': cart_key,
            'product_id': item_data.get('product_id', cart_key.split('_')[0]),
            'name': item_data['name'],
            'price': item_data['price'],
            'quantity': item_data['quantity'],
            'image': item_data.get('image', ''),
            'total': item_total,
            'color_name': item_data.get('color_name', ''),
            'color_hex':  item_data.get('color_hex', ''),
            'size':       item_data.get('size', ''),
        })
        
    discount = 0
    promo_code_obj = None
    promo_code_str = request.session.get('promo_code')
    if promo_code_str:
        from .models import PromoCode
        try:
            promo = PromoCode.objects.get(code=promo_code_str)
            if promo.is_valid:
                promo_code_obj = promo
                if promo.discount_type == 'percent':
                    discount = (subtotal * promo.discount_value) / 100
                elif promo.discount_type == 'fixed':
                    discount = promo.discount_value
            else:
                del request.session['promo_code']
        except PromoCode.DoesNotExist:
            del request.session['promo_code']
            
    total_price = max(0, subtotal - discount)
    
    return {
        'items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total_price,
        'promo_code': promo_code_obj
    }

def get_favorite_ids(request):
    favorite = get_favorites(request)
    return list(favorite.products.values_list('id', flat=True))

def cart(request):
    cart_data = get_cart_data(request)
    return render(request, 'store/cart.html', {
        'cart_items': cart_data['items'],
        'subtotal': cart_data['subtotal'],
        'discount': cart_data['discount'],
        'total_price': cart_data['total'],
        'promo_code': cart_data['promo_code'],
    })

from django.views.decorators.http import require_POST

@require_POST
def apply_promo(request):
    from .models import PromoCode
    code = request.POST.get('promo_code', '').strip().upper()
    if not code:
        messages.error(request, 'Пожалуйста, введите промокод.')
        return redirect('cart')
        
    try:
        promo = PromoCode.objects.get(code=code)
        if not promo.is_valid:
            messages.error(request, 'Этот промокод недействителен или истек.')
        else:
            request.session['promo_code'] = promo.code
            messages.success(request, f'Промокод {code} успешно применен!')
    except PromoCode.DoesNotExist:
        messages.error(request, 'Промокод не найден.')
        
    return redirect('cart')

def add_to_cart(request, product_id):
    from .models import Color, ProductImage
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    color_id  = request.POST.get('color_id', '') or ''
    size_name = request.POST.get('size', '') or ''

    # Composite key so different color/size combos are separate cart entries
    cart_key = f"{product_id}_{color_id}_{size_name}"

    # Resolve color details for display
    color_name = ''
    color_hex  = ''
    if color_id == 'original':
        if product.original_color:
            color_name = product.original_color.name
            color_hex  = product.original_color.hex_code
        else:
            color_name = 'Оригинал'
            color_hex  = '#1a1a1a'
    elif color_id and color_id not in ('', 'none'):
        try:
            color_obj  = Color.objects.get(pk=int(color_id))
            color_name = color_obj.name
            color_hex  = color_obj.hex_code
        except (Color.DoesNotExist, ValueError):
            pass

    # Use color-specific thumbnail if available, else cover
    image_url = ''
    if color_id and color_id not in ('', 'original', 'none'):
        img = ProductImage.objects.filter(product=product, color_id=color_id).first()
        if img:
            image_url = img.image.url
    if not image_url:
        image_url = product.image.url if product.image else ''

    if cart_key in cart:
        cart[cart_key]['quantity'] += 1
    else:
        cart[cart_key] = {
            'product_id': str(product_id),
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': image_url,
            'color_id': color_id,
            'color_name': color_name,
            'color_hex': color_hex,
            'size': size_name,
        }

    request.session['cart'] = cart
    label = f"{color_name or 'Оригинал'}{', ' + size_name if size_name else ''}"
    messages.success(request, f'{product.name} ({label}) добавлен в корзину!')
    next_url = request.META.get('HTTP_REFERER', 'catalog')
    return redirect(next_url)

def remove_from_cart(request, cart_key):
    cart = request.session.get('cart', {})
    if cart_key in cart:
        del cart[cart_key]
        request.session['cart'] = cart
    return redirect('cart')

def update_cart(request, cart_key):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart = request.session.get('cart', {})
        if cart_key in cart:
            if action == 'increase':
                cart[cart_key]['quantity'] += 1
            elif action == 'decrease':
                if cart[cart_key]['quantity'] > 1:
                    cart[cart_key]['quantity'] -= 1
                else:
                    del cart[cart_key]
            request.session['cart'] = cart
    return redirect('cart')

from .forms import RegistrationForm, OrderCreateForm
from .models import Category, Product, ProductImage, Favorite, Size, Color, ProductVariant, Department, Order, OrderItem

def checkout(request):
    cart_session = request.session.get('cart', {})
    if not cart_session:
        messages.error(request, 'Ваша корзина пуста.')
        return redirect('cart')

    cart_data = get_cart_data(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            # Сохраняем промокод если есть
            if cart_data['promo_code']:
                order.promo_code = cart_data['promo_code']
                
            order.save()
            
            for item in cart_data['items']:
                product = get_object_or_404(Product, id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity'],
                    color_name=item.get('color_name', ''),
                    size_name=item.get('size', ''),
                )
            
            order.total_price = cart_data['total']
            order.save()
            
            # Увеличиваем счетчик промокода
            if cart_data['promo_code']:
                promo = cart_data['promo_code']
                promo.used_count += 1
                promo.save()
            
            # Очищаем корзину и промокод
            request.session['cart'] = {}
            if 'promo_code' in request.session:
                del request.session['promo_code']
            
            if order.payment_method == 'kaspi':
                return redirect('kaspi_payment', order_id=order.id)
                
            messages.success(request, f'Заказ №{order.id} успешно оформлен! Мы свяжемся с вами в ближайшее время.')
            return redirect('index')
    else:
        # Предзаполняем данные для авторизованных пользователей
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)
        
    return render(request, 'store/checkout.html', {
        'form': form, 
        'cart': cart_session,
        'cart_items': cart_data['items'],
        'subtotal': cart_data['subtotal'],
        'discount': cart_data['discount'],
        'total_price': cart_data['total'],
        'promo_code': cart_data['promo_code'],
    })

def get_favorites(request):
    """Получить объект Favorite для текущего пользователя/сессии"""
    if request.user.is_authenticated:
        favorite, created = Favorite.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        favorite, created = Favorite.objects.get_or_create(session_id=session_id)
    return favorite

def favorites(request):
    """Страница избранного"""
    favorite = get_favorites(request)
    favorite_products = favorite.products.filter(available=True)
    
    return render(request, 'store/favorites.html', {
        'favorite_products': favorite_products,
        'total_count': favorite_products.count()
    })

def add_to_favorites(request, product_id):
    """Добавить товар в избранное"""
    product = get_object_or_404(Product, id=product_id)
    favorite = get_favorites(request)
    
    if favorite.products.filter(id=product_id).exists():
        favorite.products.remove(product)
        messages.info(request, f'{product.name} удалён из избранного')
    else:
        favorite.products.add(product)
        messages.success(request, f'{product.name} добавлен в избранное!')
    
    next_url = request.META.get('HTTP_REFERER', 'favorites')
    return redirect(next_url)

def remove_from_favorites(request, product_id):
    """Удалить товар из избранного"""
    product = get_object_or_404(Product, id=product_id)
    favorite = get_favorites(request)
    favorite.products.remove(product)
    messages.info(request, f'{product.name} удалён из избранного')
    return redirect('favorites')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                
                # Merge session favorites to user favorites
                session_id = request.session.session_key
                if session_id:
                    session_fav = Favorite.objects.filter(session_id=session_id).first()
                    if session_fav:
                        user_fav, _ = Favorite.objects.get_or_create(user=user)
                        for prod in session_fav.products.all():
                            user_fav.products.add(prod)
                        session_fav.delete()
                
                return redirect('index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

from .models import Category, Product, ProductImage, Favorite, Size, Color, ProductVariant, Department, Order, OrderItem, EmailVerification

def register_user(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Делаем неактивным до ввода кода
            user.save()
            
            import random
            from django.core.mail import send_mail
            verification_code = str(random.randint(100000, 999999))
            
            # Сохраняем код в базу
            EmailVerification.objects.create(user=user, code=verification_code)
            
            # ТЕСТИРОВАНИЕ: Выводим код в консоль
            print(f"\n{'='*50}")
            print(f"📧 КОД ПОДТВЕРЖДЕНИЯ: {verification_code}")
            print(f"   Email: {user.email}")
            print(f"{'='*50}\n")
            
            # Отправляем на почту
            try:
                send_mail(
                    'Код подтверждения регистрации QarStyle',
                    f'Ваш код подтверждения: {verification_code}',
                    'noreply@qarstyle.kz',
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                pass
            
            # ВСЕГДА ВЫВОДИМ КОД НА ЭКРАН (для тестов)
            messages.warning(request, f'Вам отправлен код (ДЛЯ ТЕСТА ОН ТУТ): {verification_code}')
                
            return redirect('verify_email')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = RegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            # Ищем код в базе
            verification = EmailVerification.objects.filter(code=code.strip()).first()
            if verification:
                user = verification.user
                user.is_active = True
                user.save()
                
                # Удаляем код после использования
                verification.delete()
                
                # Авторизуем
                from django.contrib.auth import login
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Аккаунт подтвержден! Добро пожаловать, {user.username}!')
                return redirect('index')
            else:
                messages.error(request, 'Неверный код подтверждения.')
        except Exception as e:
            messages.error(request, 'Произошла ошибка при проверке кода.')
            
    return render(request, 'store/verify_email.html')

def logout_user(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('index')

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def profile(request):
    from .forms import BodyProfileForm
    from .models import BodyProfile
    
    # Ensure profile exists
    body_profile, created = BodyProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if 'save_body_profile' in request.POST:
            form = BodyProfileForm(request.POST, instance=body_profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Параметры тела успешно сохранены!')
                return redirect('profile')
    else:
        form = BodyProfileForm(instance=body_profile)
        
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    for order in orders:
        order.update_status_if_needed()
        
    return render(request, 'store/profile.html', {
        'orders': orders,
        'body_form': form,
        'body_profile': body_profile
    })

def import_demo3(request):
    try:
        from .models import Product, Category, Department
        from django.core.files.base import ContentFile
        from django.http import HttpResponse
        import urllib.request
        import uuid
        
        mens_dept, _ = Department.objects.get_or_create(slug='mens', defaults={'name': 'Мужчины'})
        jackets_cat, _ = Category.objects.get_or_create(slug='jackets', defaults={'name': 'Куртки'})
        
        products_added = 0
        mock_data = [
            ("Rainforest Next Summer Anorak Jacket Unisex", 175.00, "https://images.napapijri.com/is/image/napapijri/NP0A4FI3RAQ1-HERO"),
            ("Traveler Jacket", 245.00, "https://images.napapijri.com/is/image/napapijri/NP0A8AMVN2D1-HERO"),
            ("Amiata Short Jacket", 175.00, "https://images.napapijri.com/is/image/napapijri/NP0A4ICTG3A1-HERO"),
            ("Rainforest Dune Anorak", 220.00, "https://images.napapijri.com/is/image/napapijri/NP0A4IKZN1Q1-HERO"),
            ("Rivalto Field Jacket", 220.00, "https://images.napapijri.com/is/image/napapijri/NP0A4HPRN2D1-HERO"),
        ]
        
        html_out = "Importing\n"
        import glob
        img_path_list = glob.glob('/Users/ais/.gemini/antigravity/brain/0c220d32-5ddb-4342-8fe5-d5ca70fe29d9/demo_jacket_1_*.png')
        if not img_path_list:
            return HttpResponse("Image not found", content_type="text/plain")
        img_path = img_path_list[0]
        
        with open(img_path, 'rb') as f:
            img_data = f.read()

        for name, price_gbp, img_base in mock_data:
            if Product.objects.filter(name=name).exists():
                continue
            price_kzt = int(price_gbp * 560)
            try:
                slug = f"napa-{uuid.uuid4().hex[:6]}"
                product = Product(
                    department=mens_dept,
                    category=jackets_cat,
                    name=name,
                    description=f"Оригинальная куртка {name} от Napapijri. Импортирована для демонстрации.",
                    price=price_kzt,
                    available=True
                )
                product.image.save(f"{slug}.png", ContentFile(img_data), save=False)
                product.save()
                products_added += 1
                html_out += f"Added: {name} ({price_kzt} KZT)\n"
            except Exception as e:
                import traceback
                html_out += f"Failed to add {name}: {str(e)}\n{traceback.format_exc()}\n"
        html_out += f"Total added: {products_added}\n"
        return HttpResponse(html_out, content_type="text/plain")
    except Exception as e:
        from django.http import HttpResponse
        return HttpResponse(f"Error: {str(e)}")

def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'Пустое сообщение'}, status=400)

            import requests
            
            gemini_key = getattr(settings, 'GEMINI_API_KEY', '')
            groq_key = getattr(settings, 'GROQ_API_KEY', '')
            
            from .models import Product
            # Pass ID to AI so it can tag recommendations
            catalog_info = "\n".join([f"- {p.name} [PRODUCT_ID:{p.id}] (Категория: {p.category.name if p.category else 'Без категории'})" for p in Product.objects.filter(available=True)[:30]])
            
            prompt = f"""Ты — умный и вежливый консультант магазина одежды QarStyle.
Отвечай кратко, естественно и ТОЛЬКО на русском языке.

Твоя база знаний (доступные товары):
{catalog_info}

ИНСТРУКЦИИ:
1. Приветствие: Если клиент здоровается, просто поздоровайся и спроси, что он ищет.
2. Поиск товара: Если клиент просит товар, который ЕСТЬ в базе знаний, напиши ОДНО короткое предложение (например: "Отличный выбор, вот что у нас есть:") и вставь теги [PRODUCT_ID:X]. НЕ пиши названия и цены текстом!
3. Отсутствие товара: Если клиент просит то, чего НЕТ в базе знаний (например, сумки, обувь, шапки), просто скажи: "К сожалению, этого товара у нас сейчас нет в наличии." И БОЛЬШЕ НИЧЕГО НЕ ПИШИ.
4. Неуместные вопросы: Если клиент задает грубые, нецензурные или странные вопросы (не про одежду) — ответь строго: "Я виртуальный консультант магазина одежды. Пожалуйста, давайте вернемся к выбору гардероба."

Вопрос клиента: {user_message}"""

            # Fallback logic to get answer
            text = None
            
            # 1. Пробуем Gemini (v1)
            try:
                g_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                g_res = requests.post(g_url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=5)
                if g_res.status_code == 200:
                    text = g_res.json()['candidates'][0]['content']['parts'][0]['text']
            except: pass

            # 2. Пробуем Groq (Llama 3.1)
            if not text:
                try:
                    q_url = "https://api.groq.com/openai/v1/chat/completions"
                    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                    q_res = requests.post(q_url, headers=headers, json={
                        "messages": [{"role": "user", "content": prompt}],
                        "model": "llama-3.1-8b-instant"
                    }, timeout=5)
                    if q_res.status_code == 200:
                        text = q_res.json()['choices'][0]['message']['content']
                except: pass

            # 3. Пробуем Groq (Mixtral)
            if not text:
                try:
                    q_url = "https://api.groq.com/openai/v1/chat/completions"
                    headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                    m_res = requests.post(q_url, headers=headers, json={
                        "messages": [{"role": "user", "content": prompt}],
                        "model": "mixtral-8x7b-32768"
                    }, timeout=5)
                    if m_res.status_code == 200:
                        text = m_res.json()['choices'][0]['message']['content']
                except: pass

            # Если всё упало - даем нормальный ответ из базы
            if not text:
                import random
                p = random.choice(list(Product.objects.filter(available=True)[:5]))
                text = f"Здравствуйте! Рекомендую обратить внимание на {p.name} [PRODUCT_ID:{p.id}]. Это отличный выбор!"

            if text:
                import re
                # Matches [PRODUCT_ID:5] or (ID: 5) or ID: 5
                product_ids = set(re.findall(r'[\[\(]?(?:PRODUCT_)?ID:\s*(\d+)[\]\)]?', text, re.IGNORECASE))
                products_data = []
                for pid in product_ids:
                    try:
                        p = Product.objects.get(id=int(pid))
                        products_data.append({
                            'id': p.id,
                            'name': p.name,
                            'price': f"{float(p.price):.0f}",
                            'image': p.image.url if p.image else '/static/store/QS.svg'
                        })
                    except Product.DoesNotExist:
                        pass
                
                # Remove tags from text
                clean_text = re.sub(r'[\[\(]?(?:PRODUCT_)?ID:\s*\d+[\]\)]?', '', text, flags=re.IGNORECASE)
                # Remove trailing colon if AI left it like "Name :"
                clean_text = re.sub(r':\s*(?=\s|$)', '', clean_text).replace('  ', ' ').strip()
                
                return JsonResponse({'response': clean_text, 'products': products_data})
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def cancel_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status == 'new':
            order.status = 'cancelled'
            order.save()
            messages.success(request, f'Заказ №{order.id} успешно отменен.')
        else:
            messages.error(request, 'Невозможно отменить заказ в текущем статусе.')
    return redirect('profile')

def kaspi_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Simulate successful payment
        if order.status == 'new':
            order.status = 'paid'
            order.save()
        messages.success(request, f'Оплата через Kaspi Pay прошла успешно! Заказ №{order.id} оформлен.')
        return redirect('index')
        
    return render(request, 'store/kaspi_payment.html', {'order': order})
