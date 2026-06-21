from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Favorite, Order, Product, Category, User

def cart_favorites_context(request):
    # ... existing code ...
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 1) for item in cart.values())

    favorites_count = 0
    if request.user.is_authenticated:
        try:
            favorite = Favorite.objects.get(user=request.user)
            favorites_count = favorite.products.filter(available=True).count()
        except Favorite.DoesNotExist:
            pass
    else:
        session_id = request.session.session_key
        if session_id:
            try:
                favorite = Favorite.objects.get(session_id=session_id)
                favorites_count = favorite.products.filter(available=True).count()
            except Favorite.DoesNotExist:
                pass

    return {
        'cart_count': cart_count,
        'favorites_count': favorites_count
    }

def admin_dashboard_context(request):
    if not request.user.is_staff:
        return {}

    # Stats
    total_revenue = Order.objects.exclude(status='cancelled').aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = Order.objects.count()
    total_clients = User.objects.count()
    total_products = Product.objects.count()

    # Latest Orders
    latest_orders = Order.objects.order_by('-created_at')[:8]

    # Categories Share (for Pie Chart)
    categories_share = Category.objects.annotate(product_count=Count('products')).values('name', 'product_count')

    # Revenue by Month (Last 6 months)
    revenue_by_month = []
    for i in range(5, -1, -1):
        month_start = (timezone.now().replace(day=1) - timedelta(days=i*30)).replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        revenue = Order.objects.filter(created_at__gte=month_start, created_at__lt=next_month).exclude(status='cancelled').aggregate(Sum('total_price'))['total_price__sum'] or 0
        revenue_by_month.append({
            'month': month_start.strftime('%b'),
            'revenue': float(revenue)
        })

    return {
        'admin_stats': {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_clients': total_clients,
            'total_products': total_products,
        },
        'latest_orders_list': latest_orders,
        'categories_share_data': list(categories_share),
        'revenue_chart_data': revenue_by_month,
    }
