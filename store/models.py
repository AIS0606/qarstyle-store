from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL-имя")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название цвета")
    hex_code = models.CharField(max_length=7, blank=True, verbose_name="Код цвета (HEX)")

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50, verbose_name="Размер")

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название отдела")
    slug = models.SlugField(unique=True, verbose_name="URL-имя")

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"

    def __str__(self):
        return self.name

class Product(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='products', null=True, blank=True, verbose_name="Отдел")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Цена (₸)")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение", blank=True, null=True)
    original_color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='original_products', verbose_name="Цвет оригинала")
    available = models.BooleanField(default=True, verbose_name="В наличии")
    is_sale = models.BooleanField(default=False, verbose_name="Распродажа")
    is_resale = models.BooleanField(default=False, verbose_name="Перепродажа")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Товар")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='images', verbose_name="Цвет")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Фотография")

    class Meta:
        verbose_name = "Фотография товара"
        verbose_name_plural = "Фотографии товара"

    def __str__(self):
        return f"Фото для {self.product.name}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name="Товар")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='variants', verbose_name="Размер")
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, related_name='variants', verbose_name="Цвет")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество")

    class Meta:
        verbose_name = "Вариация товара"
        verbose_name_plural = "Вариации товаров"

    def __str__(self):
        color_name = self.color.name if self.color else "Без цвета"
        return f"{self.product.name} - {self.size.name} - {color_name} (Остаток: {self.stock})"

class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='favorite', null=True, blank=True, verbose_name="Пользователь")
    session_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID сессии")
    products = models.ManyToManyField(Product, related_name='favorites', verbose_name="Товары")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        if self.user:
            return f"Избранное {self.user.username}"
        return f"Избранное сессии {self.session_id}"
class PromoCode(models.Model):
    DISCOUNT_TYPES = (
        ('percent', 'Процент (%)'),
        ('fixed', 'Сумма (₸)'),
    )
    code = models.CharField(max_length=50, unique=True, verbose_name="Код промокода")
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES, default='percent', verbose_name="Тип скидки")
    discount_value = models.PositiveIntegerField(verbose_name="Размер скидки")
    usage_limit = models.PositiveIntegerField(default=0, verbose_name="Лимит использований (0 - без лимита)")
    used_count = models.PositiveIntegerField(default=0, verbose_name="Использовано раз")
    valid_until = models.DateTimeField(null=True, blank=True, verbose_name="Действителен до")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ['-created_at']

    def __str__(self):
        return self.code
        
    @property
    def is_valid(self):
        from django.utils import timezone
        if not self.is_active:
            return False
        if self.usage_limit > 0 and self.used_count >= self.usage_limit:
            return False
        if self.valid_until and timezone.now() > self.valid_until:
            return False
        return True

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    )

    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Примененный промокод")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    city = models.CharField(max_length=100, verbose_name="Город")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    PAYMENT_CHOICES = (
        ('kaspi', 'Kaspi Pay'),
        ('card', 'Банковская карта онлайн'),
        ('cash', 'Наличными курьеру'),
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='kaspi', verbose_name="Способ оплаты")
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Общая сумма (₸)")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ('-created_at',)

    def __str__(self):
        return f"Заказ №{self.id} - {self.first_name} {self.last_name}"
        
    def update_status_if_needed(self):
        """
        Автоматически обновляет статус заказа на основе прошедшего времени.
        Симуляция реального цикла доставки (Paid -> Shipped -> Completed).
        """
        from django.utils import timezone
        import datetime
        
        if self.status in ['new', 'cancelled', 'completed']:
            return False  # Эти статусы не меняются автоматически
            
        now = timezone.now()
        time_passed = now - self.updated_at
        
        changed = False
        # Если статус 'paid' и прошло более 2 минут -> 'shipped'
        if self.status == 'paid' and time_passed > datetime.timedelta(minutes=2):
            self.status = 'shipped'
            changed = True
            
        # Если статус 'shipped' и прошло более 3 минут с момента ЕГО установки (то есть 5 мин с момента оплаты)
        elif self.status == 'shipped' and time_passed > datetime.timedelta(minutes=3):
            self.status = 'completed'
            changed = True
            
        if changed:
            self.save(update_fields=['status', 'updated_at'])
            return True
        return False

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Цена на момент заказа")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    color_name = models.CharField(max_length=100, blank=True, default='', verbose_name="Цвет")
    size_name = models.CharField(max_length=50, blank=True, default='', verbose_name="Размер")

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification', verbose_name="Пользователь")
    code = models.CharField(max_length=6, verbose_name="Код подтверждения")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Подтверждение почты"
        verbose_name_plural = "Подтверждения почты"

    def __str__(self):
        return f"Код для {self.user.email}"

class BodyProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='body_profile', verbose_name="Пользователь")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол", blank=True, null=True)
    height = models.PositiveIntegerField(verbose_name="Рост (см)", blank=True, null=True)
    weight = models.PositiveIntegerField(verbose_name="Вес (кг)", blank=True, null=True)
    chest = models.PositiveIntegerField(verbose_name="Обхват груди (см)", blank=True, null=True)
    waist = models.PositiveIntegerField(verbose_name="Обхват талии (см)", blank=True, null=True)
    hips = models.PositiveIntegerField(verbose_name="Обхват бедер (см)", blank=True, null=True)

    class Meta:
        verbose_name = "Параметры тела"
        verbose_name_plural = "Параметры тела"

    def __str__(self):
        return f"Параметры тела {self.user.username}"

    def get_recommended_size(self, department_slug=None):
        if not self.chest:
            return None
        
        # Logic is mostly based on chest for jackets
        if department_slug == 'mens' or self.gender == 'M':
            if self.chest <= 93: return "S"
            elif 94 <= self.chest <= 101: return "M"
            elif 102 <= self.chest <= 109: return "L"
            elif 110 <= self.chest <= 117: return "XL"
            elif self.chest >= 118: return "XXL"
        elif department_slug == 'womens' or self.gender == 'F':
            if self.chest <= 85: return "XS"
            elif 86 <= self.chest <= 89: return "S"
            elif 90 <= self.chest <= 94: return "M"
            elif 95 <= self.chest <= 101: return "L"
            elif self.chest > 101: return "XL"
            
        # Fallback if no department or gender matched specifically
        if self.chest <= 90: return "S"
        elif 91 <= self.chest <= 98: return "M"
        elif 99 <= self.chest <= 106: return "L"
        else: return "XL"

class Block(models.Model):
    TYPE_CHOICES = (
        ('hero', 'Hero-баннер (полноэкранный)'),
        ('category_pills', 'Кнопки категорий (Pills)'),
        ('two_column', 'Два блока рядом (Сплит)'),
        ('banner_cta', 'Широкий баннер с кнопкой'),
        ('cards', 'Карточки (Сетка)'),
        ('product_grid', 'Сетка реальных товаров (слайдеры, корзина)'),
        ('text', 'Текстовый блок'),
    )
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип блока")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок / Текст")
    image_main = models.ImageField(upload_to='blocks/', blank=True, null=True, verbose_name="Основная картинка / Видео")
    button_text = models.CharField(max_length=100, blank=True, verbose_name="Текст кнопки")
    button_link = models.CharField(max_length=255, blank=True, verbose_name="Ссылка кнопки")
    
    # Дополнительные поля для двухколоночного блока
    title_secondary = models.CharField(max_length=200, blank=True, verbose_name="Заголовок (2 колонка)")
    subtitle_secondary = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок (2 колонка)")
    image_secondary = models.ImageField(upload_to='blocks/', blank=True, null=True, verbose_name="Картинка (2 колонка)")
    button_text_secondary = models.CharField(max_length=100, blank=True, verbose_name="Текст кнопки (2 колонка)")
    button_link_secondary = models.CharField(max_length=255, blank=True, verbose_name="Ссылка кнопки (2 колонка)")

    class Meta:
        verbose_name = "Блок главной страницы"
        verbose_name_plural = "Блоки главной страницы"
        ordering = ['order']

    def __str__(self):
        return f"{self.get_type_display()} - {self.title or 'Без заголовка'}"

    @property
    def get_template_name(self):
        return f"store/blocks/{self.type}.html"

class BlockItem(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='items', verbose_name="Блок")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок карточки")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Подзаголовок / Подпись")
    image = models.ImageField(upload_to='blocks/items/', blank=True, null=True, verbose_name="Картинка")
    link = models.CharField(max_length=255, blank=True, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Элемент блока"
        verbose_name_plural = "Элементы блока"
        ordering = ['order']

    def __str__(self):
        return f"Элемент: {self.title or 'Без названия'} (для {self.block})"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email адрес")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписчик рассылки"
        verbose_name_plural = "Подписчики рассылки"
        ordering = ['-created_at']

    def __str__(self):
        return self.email
