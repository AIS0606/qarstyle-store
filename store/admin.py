from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Favorite, Size, Color, ProductVariant, Department, Order, OrderItem

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'hex_code': forms.TextInput(attrs={'type': 'color', 'style': 'width:40px; height:40px; padding:0; border:none; border-radius:4px;'}),
        }

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    form = ColorForm
    list_display = ['name', 'color_swatch', 'hex_code']

    def color_swatch(self, obj):
        if obj.hex_code:
            return format_html('<div style="width: 24px; height: 24px; background-color: {}; border: 1px solid #ccc; border-radius: 50%;"></div>', obj.hex_code)
        return "-"
    color_swatch.short_description = "Цвет"

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 20

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'department', 'category', 'is_sale', 'is_resale', 'available']
    list_filter = ['department', 'category', 'is_sale', 'is_resale', 'available']
    list_editable = ['price', 'is_sale', 'is_resale', 'available']
    inlines = [ProductVariantInline, ProductImageInline]

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['get_user_or_session', 'get_product_count']
    filter_horizontal = ('products',)
    
    def get_user_or_session(self, obj):
        if obj.user:
            return f"Пользователь: {obj.user.username}"
        return f"Сессия: {obj.session_id}"
    get_user_or_session.short_description = "Пользователь/Сессия"
    
    def get_product_count(self, obj):
        return obj.products.count()
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Переопределяем стандартную админку пользователей, чтобы видеть их как "Клиентов"
admin.site.unregister(User)
@admin.register(User)
class CustomerAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    ordering = ('-date_joined',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    list_editable = ['status']
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email', 'phone']

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import Block, BlockItem

class BlockItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = BlockItem
    extra = 0

@admin.register(Block)
class BlockAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'type', 'is_active', 'order')
    list_filter = ('type', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title', 'subtitle')
    inlines = [BlockItemInline]
    
    fieldsets = (
        ('Основные настройки', {
            'fields': ('type', 'is_active', 'title', 'subtitle', 'image_main', 'button_text', 'button_link')
        }),
        ('Вторая колонка (Только для типа "Два блока рядом")', {
            'classes': ('collapse',),
            'fields': ('title_secondary', 'subtitle_secondary', 'image_secondary', 'button_text_secondary', 'button_link_secondary')
        }),
    )
