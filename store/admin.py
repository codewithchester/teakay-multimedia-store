from django.contrib import admin
from admincharts.admin import AdminChartMixin
from .models import Product, Order, OrderItem

# Register Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')

# Register OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

# Register Order with Chart
@admin.register(Order)
class OrderAdmin(AdminChartMixin, admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'paid', 'created_at')
    list_filter = ('paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    
    # Chart settings
    list_chart_title = "Orders Overview"
    list_chart_type = "bar"  # 'bar', 'line', 'pie', 'doughnut'
    
    def get_list_chart_data(self, queryset):
        """Generate chart data"""
        if not queryset.exists():
            return {
                "labels": ["No Data"],
                "datasets": [{
                    "label": "Orders",
                    "data": [0],
                    "backgroundColor": "#cccccc",
                }]
            }
        
        # Count orders by month
        months = {}
        for order in queryset:
            month_key = order.created_at.strftime('%b %Y')
            months[month_key] = months.get(month_key, 0) + 1
        
        # Sort by date
        import datetime
        sorted_months = sorted(months.items(), key=lambda x: datetime.datetime.strptime(x[0], '%b %Y'))
        
        labels = [item[0] for item in sorted_months]
        data = [item[1] for item in sorted_months]
        
        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Orders",
                    "data": data,
                    "backgroundColor": [
                        "#3498db", "#2ecc71", "#e74c3c", 
                        "#f39c12", "#9b59b6", "#1abc9c",
                        "#e67e22", "#34495e", "#95a5a6"
                    ][:len(data)],
                }
            ],
        }