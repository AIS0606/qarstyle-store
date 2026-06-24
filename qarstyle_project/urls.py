"""
URL configuration for qarstyle_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import admin_views

from django.views.generic import RedirectView

urlpatterns = [
    # Custom dashboard routes (take precedence)
    path('admin/', RedirectView.as_view(url='/admin/overview/', permanent=False)),
    path('admin/overview/', admin_views.admin_overview, name='custom_admin_overview'),
    path('admin/analytics/', admin_views.admin_analytics, name='custom_admin_analytics'),
    path('admin/store/product/', admin_views.admin_products_list, name='custom_admin_products'),
    path('admin/store/product/add/', admin_views.admin_product_add, name='custom_admin_product_add'),
    path('admin/store/product/<int:product_id>/edit/', admin_views.admin_product_edit, name='custom_admin_product_edit'),
    path('admin/store/product/<int:product_id>/delete/', admin_views.admin_product_delete, name='custom_admin_product_delete'),
    path('admin/store/order/', admin_views.admin_orders_list, name='custom_admin_orders'),
    path('admin/store/order/<int:order_id>/update-status/', admin_views.admin_order_update_status, name='custom_admin_order_update_status'),
    path('admin/store/category/', admin_views.admin_categories_list, name='custom_admin_categories'),
    path('admin/auth/user/', admin_views.admin_clients_list, name='custom_admin_clients'),
    path('admin/marketing/', admin_views.admin_marketing, name='custom_admin_marketing'),
    path('admin/settings/', admin_views.admin_settings, name='custom_admin_settings'),
    
    # Custom block routing
    path('admin/store/block/', admin_views.admin_blocks_list, name='custom_admin_blocks'),
    path('admin/store/block/add/', admin_views.admin_block_add, name='custom_admin_block_add'),
    path('admin/store/block/<int:block_id>/edit/', admin_views.admin_block_edit, name='custom_admin_block_edit'),
    path('admin/store/block/<int:block_id>/delete/', admin_views.admin_block_delete, name='custom_admin_block_delete'),
    path('admin/store/block/reorder/', admin_views.admin_blocks_reorder, name='admin_blocks_reorder'),
    path('admin/store/block/api/reorder/', admin_views.api_block_reorder, name='api_block_reorder'),
    
    # Block Item API
    path('admin/store/block/<int:block_id>/items/add/', admin_views.api_blockitem_add, name='api_blockitem_add'),
    path('admin/store/blockitem/<int:item_id>/save/', admin_views.api_blockitem_save, name='api_blockitem_save'),
    path('admin/store/blockitem/<int:item_id>/delete/', admin_views.api_blockitem_delete, name='api_blockitem_delete'),
    path('admin/store/block/<int:block_id>/items/reorder/', admin_views.api_blockitem_reorder, name='api_blockitem_reorder'),
    
    # Default admin routing
    path('admin/', admin.site.urls),
    
    path('accounts/', include('allauth.urls')),
    path('', include('store.urls')),
    
    # Newsletter
    path('newsletter/subscribe/', admin_views.subscribe_newsletter, name='subscribe_newsletter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
