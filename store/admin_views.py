from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from django.db import models
from .models import Order, Product, Category, Department, User, OrderItem, ProductVariant, Size, Color, ProductImage

@staff_member_required
def admin_overview(request):
    total_revenue = Order.objects.exclude(status='cancelled').aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = Order.objects.count()
    total_clients = User.objects.count()
    total_products = Product.objects.count()

    latest_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    
    # Top products by number of times ordered
    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).filter(total_sold__gt=0).order_by('-total_sold')[:5]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_clients': total_clients,
        'total_products': total_products,
        'latest_orders': latest_orders,
        'top_products': top_products,
    }
    return render(request, 'admin/overview.html', context)

@staff_member_required
def admin_analytics(request):
    total_revenue = Order.objects.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = Order.objects.filter(status='completed').count()
    avg_check = int(total_revenue / total_orders) if total_orders > 0 else 0
    
    cities_data = Order.objects.filter(status='completed').values('city').annotate(
        order_count=Count('id'), 
        total=Sum('total_price')
    ).order_by('-total')[:6]

    # Categories share
    categories = Category.objects.annotate(product_count=Count('products')).values('name', 'product_count')
    total_prods_for_share = sum(c['product_count'] for c in categories) or 1
    categories_share = [
        {'name': c['name'], 'percentage': int((c['product_count'] / total_prods_for_share) * 100), 'color': ''}
        for c in categories
    ]
    categories_share = sorted(categories_share, key=lambda x: x['percentage'], reverse=True)[:5]
    colors = ['#000', '#333', '#666', '#999', '#ccc']
    for i, c in enumerate(categories_share):
        c['color'] = colors[i]

    context = {
        'total_revenue': total_revenue,
        'avg_check': avg_check,
        'conversion': 3.8,  # Mocked
        'ltv': 1240000,     # Mocked
        'cities_data': cities_data,
        'categories_share': categories_share
    }
    return render(request, 'admin/analytics.html', context)

@staff_member_required
def admin_products_list(request):
    from django.core.paginator import Paginator

    products = Product.objects.select_related('category', 'department').annotate(
        total_stock=Sum('variants__stock'),
        total_sold=Sum('orderitem__quantity')
    ).order_by('-id')

    # Вкладки отделов
    department_slug = request.GET.get('department', 'all')
    if department_slug != 'all':
        if department_slug == 'unisex':
            # Допустим, если нет отдела, это унисекс (или можно игнорировать)
            products = products.filter(department__isnull=True)
        else:
            products = products.filter(department__slug=department_slug)

    # Поиск
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(category__name__icontains=search_query) |
            Q(id__icontains=search_query.replace('QS-PROD-', ''))
        )

    # Вид
    view_mode = request.GET.get('view', 'list')

    # Статистика (считаем до пагинации)
    total = products.count()
    
    # Для in_stock, low_stock, out_of_stock мы используем total_stock из annotate
    # Чтобы использовать его в filter, нужно либо вычислять в памяти, либо через filter после annotate
    in_stock = len([p for p in products if p.total_stock and p.total_stock > 0 and p.available])
    low_stock = len([p for p in products if p.total_stock and 0 < p.total_stock < 20])
    out_of_stock = len([p for p in products if not p.total_stock or p.total_stock == 0 or not p.available])

    # Пагинация
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'total': total,
        'in_stock': in_stock,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'search_query': search_query,
        'department_slug': department_slug,
        'view_mode': view_mode
    }
    return render(request, 'admin/products_list.html', context)

@staff_member_required
def admin_product_add(request):
    categories = Category.objects.all()
    departments = Department.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.method == 'POST':
        product = Product(
            name=request.POST.get('name', 'Без названия'),
            description=request.POST.get('description', ''),
            price=request.POST.get('price', 0),
            available=request.POST.get('available') == 'on',
            is_sale=request.POST.get('is_sale') == 'on',
            is_resale=request.POST.get('is_resale') == 'on'
        )

        category_id = request.POST.get('category')
        if category_id:
            product.category_id = category_id
        department_id = request.POST.get('department')
        product.department_id = department_id if department_id else None

        new_original_color_name = request.POST.get('new_original_color_name', '').strip()
        if new_original_color_name:
            new_original_color_hex = request.POST.get('new_original_color_hex', '#aa7942').strip()
            color, _ = Color.objects.get_or_create(
                name=new_original_color_name,
                defaults={'hex_code': new_original_color_hex}
            )
            product.original_color = color
        else:
            original_color_id = request.POST.get('original_color')
            product.original_color_id = original_color_id if original_color_id else None

        if request.FILES.get('cover_image'):
            product.image = request.FILES['cover_image']
        product.save()

        # Extra images (no color)
        for f in request.FILES.getlist('extra_images'):
            ProductImage.objects.create(product=product, image=f, color=None)

        # Color variant blocks
        color_block_ids = request.POST.getlist('color_block_id')
        for color_id in color_block_ids:
            if not color_id:
                continue

            if str(color_id).startswith('new_'):
                color_name = request.POST.get(f'new_color_name_{color_id}', '').strip()
                color_hex  = request.POST.get(f'new_color_hex_{color_id}', '').strip()
                if not color_name:
                    continue
                color, _ = Color.objects.get_or_create(
                    name=color_name,
                    defaults={'hex_code': color_hex}
                )
            else:
                try:
                    color = Color.objects.get(pk=color_id)
                except Color.DoesNotExist:
                    continue

            for f in request.FILES.getlist(f'color_photos_{color_id}'):
                ProductImage.objects.create(product=product, image=f, color=color)

            for size in sizes:
                stock_key = f'stock_{color_id}_{size.id}'
                stock_val = request.POST.get(stock_key, '').strip()
                if stock_val != '':
                    try:
                        stock = max(0, int(stock_val))
                        ProductVariant.objects.update_or_create(
                            product=product, color=color, size=size,
                            defaults={'stock': stock}
                        )
                    except ValueError:
                        pass

        # Base sizes (no color)
        for size in sizes:
            stock_key = f'stock_base_{size.id}'
            stock_val = request.POST.get(stock_key, '').strip()
            if stock_val != '':
                try:
                    stock = max(0, int(stock_val))
                    ProductVariant.objects.update_or_create(
                        product=product, color=None, size=size,
                        defaults={'stock': stock}
                    )
                except ValueError:
                    pass

        messages.success(request, f'Товар «{product.name}» успешно добавлен.')
        return redirect('custom_admin_product_edit', product_id=product.id)

    base_sizes = [{'size': s, 'stock': ''} for s in sizes]

    context = {
        'product': None,
        'categories': categories,
        'departments': departments,
        'sizes': sizes,
        'colors': colors,
        'base_sizes': base_sizes,
        'color_blocks': [],
        'extra_images': [],
    }
    return render(request, 'admin/product_edit.html', context)

@staff_member_required
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()
    departments = Department.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.method == 'POST':
        # Basic fields
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.price = request.POST.get('price', product.price)
        product.available = request.POST.get('available') == 'on'
        product.is_sale = request.POST.get('is_sale') == 'on'
        product.is_resale = request.POST.get('is_resale') == 'on'

        category_id = request.POST.get('category')
        if category_id:
            product.category_id = category_id
        department_id = request.POST.get('department')
        product.department_id = department_id if department_id else None

        new_original_color_name = request.POST.get('new_original_color_name', '').strip()
        if new_original_color_name:
            new_original_color_hex = request.POST.get('new_original_color_hex', '#aa7942').strip()
            color, _ = Color.objects.get_or_create(
                name=new_original_color_name,
                defaults={'hex_code': new_original_color_hex}
            )
            product.original_color = color
        else:
            original_color_id = request.POST.get('original_color')
            product.original_color_id = original_color_id if original_color_id else None

        # Delete color blocks if requested
        delete_color_ids = request.POST.getlist('delete_color_id')
        for delete_color_id in delete_color_ids:
            if delete_color_id and not str(delete_color_id).startswith('new_'):
                try:
                    ProductVariant.objects.filter(product=product, color_id=int(delete_color_id)).delete()
                    ProductImage.objects.filter(product=product, color_id=int(delete_color_id)).delete()
                except ValueError:
                    pass

        # Cover image
        if request.FILES.get('cover_image'):
            product.image = request.FILES['cover_image']
        product.save()

        # Extra images (no color)
        for f in request.FILES.getlist('extra_images'):
            ProductImage.objects.create(product=product, image=f, color=None)

        # Delete extra images if requested
        for img_id in request.POST.getlist('delete_extra_image'):
            ProductImage.objects.filter(pk=img_id, product=product, color__isnull=True).delete()

        # Color variant blocks
        color_block_ids = request.POST.getlist('color_block_id')
        for color_id in color_block_ids:
            if not color_id:
                continue

            # Create new color if ID starts with "new_"
            if str(color_id).startswith('new_'):
                color_name = request.POST.get(f'new_color_name_{color_id}', '').strip()
                color_hex  = request.POST.get(f'new_color_hex_{color_id}', '').strip()
                if not color_name:
                    continue
                color, _ = Color.objects.get_or_create(
                    name=color_name,
                    defaults={'hex_code': color_hex}
                )
            else:
                try:
                    color = Color.objects.get(pk=color_id)
                except Color.DoesNotExist:
                    continue

            # Photos for this color
            for f in request.FILES.getlist(f'color_photos_{color_id}'):
                ProductImage.objects.create(product=product, image=f, color=color)

            # Delete color photos if requested
            for img_id in request.POST.getlist(f'delete_color_image_{color_id}'):
                ProductImage.objects.filter(pk=img_id, product=product, color=color).delete()

            # Size stocks for this color
            for size in sizes:
                stock_key = f'stock_{color_id}_{size.id}'
                stock_val = request.POST.get(stock_key, '').strip()
                if stock_val != '':
                    try:
                        stock = max(0, int(stock_val))
                        ProductVariant.objects.update_or_create(
                            product=product, color=color, size=size,
                            defaults={'stock': stock}
                        )
                    except ValueError:
                        pass
                else:
                    ProductVariant.objects.filter(product=product, color=color, size=size).delete()

        # Base sizes (no color)
        for size in sizes:
            stock_key = f'stock_base_{size.id}'
            stock_val = request.POST.get(stock_key, '').strip()
            if stock_val != '':
                try:
                    stock = max(0, int(stock_val))
                    ProductVariant.objects.update_or_create(
                        product=product, color=None, size=size,
                        defaults={'stock': stock}
                    )
                except ValueError:
                    pass
            else:
                ProductVariant.objects.filter(product=product, color__isnull=True, size=size).delete()

        messages.success(request, f'Товар «{product.name}» успешно сохранён.')
        return redirect('custom_admin_product_edit', product_id=product.id)

    # GET — build context
    PI = ProductImage
    variants = ProductVariant.objects.filter(product=product).select_related('size', 'color')
    extra_images = PI.objects.filter(product=product, color__isnull=True)
    color_images = PI.objects.filter(product=product, color__isnull=False).select_related('color')

    # Collect colors from BOTH variants AND color-specific images so nothing gets lost
    variant_color_ids = set(variants.filter(color__isnull=False).values_list('color_id', flat=True))
    image_color_ids   = set(color_images.values_list('color_id', flat=True))
    all_color_ids     = variant_color_ids | image_color_ids
    product_colors    = Color.objects.filter(pk__in=all_color_ids)

    # Base sizes (no color)
    base_stocks = {v.size_id: v.stock for v in variants.filter(color__isnull=True)}
    base_sizes = [{'size': s, 'stock': base_stocks.get(s.id, '')} for s in sizes]

    color_blocks = []
    for color in product_colors:
        color_stocks = {v.size_id: v.stock for v in variants.filter(color=color)}
        sizes_with_stock = [{'size': s, 'stock': color_stocks.get(s.id, '')} for s in sizes]
        color_imgs = list(color_images.filter(color=color))
        color_blocks.append({
            'color': color,
            'sizes': sizes_with_stock,
            'images': color_imgs,
        })

    context = {
        'product': product,
        'categories': categories,
        'departments': departments,
        'sizes': sizes,
        'colors': colors,
        'base_sizes': base_sizes,
        'color_blocks': color_blocks,
        'extra_images': extra_images,
    }
    return render(request, 'admin/product_edit.html', context)

@staff_member_required
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'Товар «{product.name}» удален.')
    return redirect('custom_admin_products')

@staff_member_required
def admin_orders_list(request):
    from django.core.paginator import Paginator

    orders = Order.objects.prefetch_related('items__product__category').all().order_by('-created_at')

    # Поиск
    search_query = request.GET.get('q', '').strip()
    if search_query:
        orders = orders.filter(
            Q(id__icontains=search_query.replace('QS-', '')) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Фильтр по статусу
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    # Статистика (общая, без учета фильтра)
    all_orders = Order.objects.all()
    total = all_orders.count()
    delivered = all_orders.filter(status='completed').count()
    in_transit = all_orders.filter(status='shipped').count()
    processing = all_orders.filter(status='paid').count() + all_orders.filter(status='new').count()
    cancelled = all_orders.filter(status='cancelled').count()

    # Пагинация
    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
        'page_obj': page_obj,
        'total': total,
        'delivered': delivered,
        'in_transit': in_transit,
        'processing': processing,
        'cancelled': cancelled,
        'search_query': search_query,
        'status_filter': status_filter
    }
    return render(request, 'admin/orders_list.html', context)

@staff_member_required
def admin_order_update_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=order_id)
        new_status = request.POST.get('status')
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            messages.success(request, f'Статус заказа QS-{order.id} изменен на "{order.get_status_display()}".')
    
    return redirect(request.META.get('HTTP_REFERER', 'custom_admin_orders'))

@staff_member_required
def admin_categories_list(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_category':
            name = request.POST.get('name')
            slug = request.POST.get('slug')
            if name and slug:
                Category.objects.create(name=name, slug=slug)
                messages.success(request, f'Категория "{name}" успешно добавлена.')
                return redirect('custom_admin_categories')

    departments = Department.objects.all()
    dept_data = []

    # Get categories that have products in this department
    for dept in departments:
        cats_in_dept = Category.objects.filter(products__department=dept).annotate(
            dept_product_count=Count('products', filter=Q(products__department=dept), distinct=True)
        ).distinct()
        
        cats_list = []
        for cat in cats_in_dept:
            sales = OrderItem.objects.filter(
                product__category=cat,
                product__department=dept,
                order__status='completed'
            ).aggregate(total=Sum(models.F('price') * models.F('quantity')))['total'] or 0
            
            cats_list.append({
                'id': f"{dept.id}_{cat.id}",
                'original_id': cat.id,
                'name': cat.name,
                'slug': cat.slug,
                'product_count': cat.dept_product_count,
                'sales': sales,
                'products': Product.objects.filter(department=dept, category=cat)[:5],
                'total_products': cat.dept_product_count,
            })
            
        dept_data.append({
            'id': dept.id,
            'name': dept.name,
            'slug': dept.slug,
            'categories': cats_list
        })
        
    # Categories with no products at all
    empty_categories = Category.objects.annotate(prod_count=Count('products')).filter(prod_count=0)
    empty_cats_list = []
    for cat in empty_categories:
        empty_cats_list.append({
            'id': f"empty_{cat.id}",
            'original_id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'product_count': 0,
            'sales': 0,
            'products': [],
            'total_products': 0,
        })

    context = {
        'departments': dept_data,
        'empty_categories': empty_cats_list,
    }
    return render(request, 'admin/categories_list.html', context)

@staff_member_required
def admin_clients_list(request):
    clients = User.objects.annotate(
        orders_count=Count('order', filter=Q(order__status='completed')),
        total_spent=Sum('order__total_price', filter=Q(order__status='completed')),
        last_order=models.Max('order__created_at')
    ).order_by('-date_joined')
    
    # Calculate tiers in python for simplicity (can be done in DB but simpler here)
    for client in clients:
        client.total_spent = client.total_spent or 0
        if client.total_spent > 1000000:
            client.tier = 'VIP'
        elif client.orders_count >= 5:
            client.tier = 'Постоянный'
        elif client.orders_count > 0:
            client.tier = 'Обычный'
        else:
            client.tier = 'Новый'
            
        # Get city from latest order
        latest_order = client.order_set.order_by('-created_at').first()
        client.city = latest_order.city if latest_order else 'Не указан'
        client.phone = latest_order.phone if latest_order else 'Не указан'

    total = clients.count()
    vip_count = sum(1 for c in clients if c.tier == 'VIP')
    regular_count = sum(1 for c in clients if c.tier == 'Постоянный')
    normal_count = sum(1 for c in clients if c.tier == 'Обычный')
    new_count = sum(1 for c in clients if c.tier == 'Новый')
    
    context = {
        'clients': clients[:15],
        'total': total,
        'vip_count': vip_count,
        'regular_count': regular_count,
        'normal_count': normal_count,
        'new_count': new_count,
    }
    return render(request, 'admin/clients_list.html', context)

@staff_member_required
def admin_marketing(request):
    from .models import NewsletterSubscriber
    from django.core.mail import send_mass_mail
    from django.conf import settings
    from django.contrib import messages
    
    subscribers_count = NewsletterSubscriber.objects.filter(is_active=True).count()
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if subject and message:
            subscribers = NewsletterSubscriber.objects.filter(is_active=True).values_list('email', flat=True)
            if subscribers:
                messages_tuple = (
                    (subject, message, settings.DEFAULT_FROM_EMAIL, [email]) 
                    for email in subscribers
                )
                try:
                    send_mass_mail(messages_tuple, fail_silently=False)
                    messages.success(request, f'Рассылка успешно отправлена {len(subscribers)} подписчикам!')
                except Exception as e:
                    messages.error(request, f'Ошибка при отправке: {str(e)}')
            else:
                messages.error(request, 'Нет активных подписчиков для рассылки.')
        else:
            messages.error(request, 'Тема и текст письма обязательны.')

    promos = [
        {"code": "SUMMER26", "type": "Процент", "value": "15%", "used": 47, "limit": 100, "expiry": "31 июля 2026", "status": "Активен"},
        {"code": "WELCOME", "type": "Фиксированная", "value": "5 000 ₸", "used": 234, "limit": 500, "expiry": "Бессрочно", "status": "Активен"},
        {"code": "VIP2026", "type": "Процент", "value": "20%", "used": 89, "limit": 200, "expiry": "31 декабря 2026", "status": "Активен"},
        {"code": "SPRING25", "type": "Процент", "value": "10%", "used": 312, "limit": 300, "expiry": "30 апреля 2025", "status": "Истёк"},
    ]
    
    campaigns = [
        {"name": "Летняя коллекция 2026", "type": "Email", "sent": 3240, "opened": 1247, "clicks": 389, "orders": 67, "status": "Отправлено"},
        {"name": "Новинки мужской", "type": "Push", "sent": 1840, "opened": 892, "clicks": 234, "orders": 41, "status": "Отправлено"},
        {"name": "VIP предложение", "type": "Email", "sent": 127, "opened": 98, "clicks": 72, "orders": 28, "status": "Запланировано"},
    ]
    
    context = {
        'promos': promos,
        'campaigns': campaigns,
        'subscribers_count': subscribers_count
    }
    return render(request, 'admin/marketing.html', context)

@staff_member_required
def admin_block_add(request):
    from .models import Block, BlockItem
    if request.method == 'POST':
        block = Block.objects.create(
            type=request.POST.get('type'),
            title=request.POST.get('title'),
            subtitle=request.POST.get('subtitle'),
            button_text=request.POST.get('button_text'),
            button_link=request.POST.get('button_link'),
            title_secondary=request.POST.get('title_secondary'),
            subtitle_secondary=request.POST.get('subtitle_secondary'),
            button_text_secondary=request.POST.get('button_text_secondary'),
            button_link_secondary=request.POST.get('button_link_secondary'),
            is_active=request.POST.get('is_active') == 'on',
            order=Block.objects.count() + 1
        )
        if 'image_main' in request.FILES: block.image_main = request.FILES['image_main']
        if 'image_secondary' in request.FILES: block.image_secondary = request.FILES['image_secondary']
        block.save()
        messages.success(request, 'Блок успешно добавлен.')
        return redirect('custom_admin_blocks')
    return render(request, 'admin/block_edit.html', {'types': Block.TYPE_CHOICES})

@staff_member_required
def admin_block_edit(request, block_id):
    from .models import Block, BlockItem
    block = get_object_or_404(Block, id=block_id)
    if request.method == 'POST':
        block.type = request.POST.get('type')
        block.title = request.POST.get('title')
        block.subtitle = request.POST.get('subtitle')
        block.button_text = request.POST.get('button_text')
        block.button_link = request.POST.get('button_link')
        block.title_secondary = request.POST.get('title_secondary')
        block.subtitle_secondary = request.POST.get('subtitle_secondary')
        block.button_text_secondary = request.POST.get('button_text_secondary')
        block.button_link_secondary = request.POST.get('button_link_secondary')
        block.is_active = request.POST.get('is_active') == 'on'
        if 'image_main' in request.FILES: block.image_main = request.FILES['image_main']
        if 'image_secondary' in request.FILES: block.image_secondary = request.FILES['image_secondary']
        block.save()
        messages.success(request, 'Блок успешно обновлен.')
        return redirect('custom_admin_blocks')
    return render(request, 'admin/block_edit.html', {'block': block, 'types': Block.TYPE_CHOICES})

@staff_member_required
def admin_block_delete(request, block_id):
    from .models import Block
    block = get_object_or_404(Block, id=block_id)
    block.delete()
    messages.success(request, 'Блок удален.')
    return redirect('custom_admin_blocks')

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@staff_member_required
def admin_blocks_reorder(request):
    from .models import Block
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_list = data.get('order', [])
            for index, block_id in enumerate(order_list):
                Block.objects.filter(id=block_id).update(order=index)
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

@staff_member_required
def admin_blocks_list(request):
    from .models import Block
    blocks = Block.objects.all().order_by('order')
    return render(request, 'admin/blocks_list.html', {'blocks': blocks, 'types': Block.TYPE_CHOICES})

@staff_member_required
def api_block_get(request, block_id):
    from .models import Block
    block = get_object_or_404(Block, id=block_id)
    data = {
        'id': block.id,
        'type': block.type,
        'is_active': block.is_active,
        'title': block.title,
        'subtitle': block.subtitle,
        'button_text': block.button_text,
        'button_link': block.button_link,
        'title_secondary': block.title_secondary,
        'subtitle_secondary': block.subtitle_secondary,
        'button_text_secondary': block.button_text_secondary,
        'button_link_secondary': block.button_link_secondary,
        'image_main_url': block.image_main.url if block.image_main else None,
        'image_secondary_url': block.image_secondary.url if block.image_secondary else None,
        'items': [{
            'id': item.id,
            'title': item.title,
            'subtitle': item.subtitle,
            'link': item.link,
            'order': item.order,
            'image_url': item.image.url if item.image else None
        } for item in block.items.all().order_by('order')]
    }
    return JsonResponse({'status': 'ok', 'block': data})

@staff_member_required
def api_block_save(request, block_id):
    from .models import Block
    block = get_object_or_404(Block, id=block_id)
    if request.method == 'POST':
        block.type = request.POST.get('type', block.type)
        block.title = request.POST.get('title', '')
        block.subtitle = request.POST.get('subtitle', '')
        block.button_text = request.POST.get('button_text', '')
        block.button_link = request.POST.get('button_link', '')
        block.title_secondary = request.POST.get('title_secondary', '')
        block.subtitle_secondary = request.POST.get('subtitle_secondary', '')
        block.button_text_secondary = request.POST.get('button_text_secondary', '')
        block.button_link_secondary = request.POST.get('button_link_secondary', '')
        
        is_active_val = request.POST.get('is_active')
        if is_active_val is not None:
            block.is_active = is_active_val == 'true'
            
        if 'image_main' in request.FILES:
            block.image_main = request.FILES['image_main']
        if 'image_secondary' in request.FILES:
            block.image_secondary = request.FILES['image_secondary']
            
        block.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_block_add(request):
    from .models import Block
    if request.method == 'POST':
        type = request.POST.get('type', 'hero')
        order = int(request.POST.get('order', Block.objects.count() + 1))
        # Shift blocks down if inserting
        Block.objects.filter(order__gte=order).update(order=models.F('order') + 1)
        
        block = Block.objects.create(type=type, order=order, is_active=True, title="Новый блок")
        return JsonResponse({'status': 'ok', 'block_id': block.id})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_block_delete(request, block_id):
    from .models import Block
    if request.method == 'POST':
        block = get_object_or_404(Block, id=block_id)
        block.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
@csrf_exempt
def api_block_reorder(request):
    from .models import Block
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        order_list = data.get('order', [])
        for index, block_id in enumerate(order_list):
            Block.objects.filter(id=block_id).update(order=index)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_blockitem_add(request, block_id):
    from .models import Block, BlockItem
    if request.method == 'POST':
        block = get_object_or_404(Block, id=block_id)
        last_order = block.items.count()
        item = BlockItem.objects.create(block=block, title="Новая карточка", order=last_order+1)
        return JsonResponse({'status': 'ok', 'item_id': item.id})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_blockitem_save(request, item_id):
    from .models import BlockItem
    item = get_object_or_404(BlockItem, id=item_id)
    if request.method == 'POST':
        item.title = request.POST.get('title', '')
        item.subtitle = request.POST.get('subtitle', '')
        item.link = request.POST.get('link', '')
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        item.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
def api_blockitem_delete(request, item_id):
    from .models import BlockItem
    if request.method == 'POST':
        item = get_object_or_404(BlockItem, id=item_id)
        item.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
@csrf_exempt
def api_blockitem_reorder(request, block_id):
    from .models import BlockItem
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        order_list = data.get('order', [])
        for index, item_id in enumerate(order_list):
            BlockItem.objects.filter(id=item_id, block_id=block_id).update(order=index)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@staff_member_required
def admin_settings(request):
    return render(request, 'admin/settings.html')

from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse

@require_POST
def subscribe_newsletter(request):
    from .models import NewsletterSubscriber
    email = request.POST.get('email', '').strip()
    
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email обязателен'}, status=400)
        
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'status': 'error', 'message': 'Некорректный email'}, status=400)
        
    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={'is_active': True}
    )
    
    if not created and not subscriber.is_active:
        subscriber.is_active = True
        subscriber.save()
        
    return JsonResponse({'status': 'success', 'message': 'Вы успешно подписались на рассылку!'})
