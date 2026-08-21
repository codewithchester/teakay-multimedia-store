from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order, Product
from datetime import datetime
import json

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard with analytics"""
    
    # Basic stats
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    paid_orders = Order.objects.filter(paid=True).count()
    unpaid_orders = Order.objects.filter(paid=False).count()
    
    # Orders by month (for chart)
    months = {}
    for order in Order.objects.all():
        month_key = order.created_at.strftime('%b %Y')
        months[month_key] = months.get(month_key, 0) + 1
    
    # Sort months
    sorted_months = sorted(months.items(), key=lambda x: datetime.strptime(x[0], '%b %Y'))
    
    chart_labels = json.dumps([item[0] for item in sorted_months])
    chart_data = json.dumps([item[1] for item in sorted_months])
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'paid_orders': paid_orders,
        'unpaid_orders': unpaid_orders,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin/dashboard.html', context)