from django.urls import path
from . import views
from . import views_demo

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<str:cart_key>/', views.update_cart, name='update_cart'),
    path('cart/apply-promo/', views.apply_promo, name='apply_promo'),
    path('remove-from-cart/<str:cart_key>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('favorites/', views.favorites, name='favorites'),
    path('add-to-favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('ai-chat/', views.ai_chat, name='ai_chat'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('kaspi-payment/<int:order_id>/', views.kaspi_payment, name='kaspi_payment'),
]
