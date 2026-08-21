from django.contrib import admin
from admincharts.admin import AdminChartMixin
from .models import Product, Order, OrderItem


# ─── PRODUCT ADMIN ───
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    
    # Jazzmin fieldsets for better UI
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'price', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)  # Collapsible section
        }),
    )


# ─── ORDER ITEM ADMIN ───
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_price')
    list_filter = ('order',)
    search_fields = ('product__name', 'order__email')
    
    def total_price(self, obj):
        return obj.price * obj.quantity
    total_price.short_description = "Total"


# ─── ORDER ADMIN WITH CHART ───
@admin.register(Order)
class OrderAdmin(AdminChartMixin, admin.ModelAdmin):
    # ── List Display ──
    list_display = ('id', 'customer_name', 'email', 'phone', 'paid', 'created_at')
    list_filter = ('paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    # ── Jazzmin Fieldsets ──
    fieldsets = (
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address')
        }),
        ('Order Status', {
            'fields': ('paid',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    # ── Chart Settings ──
    list_chart_title = "📊 Orders Overview"
    list_chart_type = "bar"
    list_chart_height = 300
    
    # ── Custom Methods ──
    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = "Customer"
    customer_name.admin_order_field = 'first_name'
    
    # ── Chart Data ──
    def get_list_chart_data(self, queryset):
        """Generate chart data for orders by month"""
        if not queryset.exists():
            return {
                "labels": ["No Data"],
                "datasets": [{
                    "label": "Orders",
                    "data": [0],
                    "backgroundColor": ["#cccccc"],
                }]
            }
        
        # Count orders by month
        months = {}
        for order in queryset:
            month_key = order.created_at.strftime('%b %Y')
            months[month_key] = months.get(month_key, 0) + 1
        
        # Sort by date
        import datetime
        sorted_months = sorted(
            months.items(), 
            key=lambda x: datetime.datetime.strptime(x[0], '%b %Y')
        )
        
        labels = [item[0] for item in sorted_months]
        data = [item[1] for item in sorted_months]
        
        # Color palette
        colors = [
            "#4f46e5", "#7c3aed", "#ec4899", 
            "#f59e0b", "#10b981", "#06b6d4",
            "#ef4444", "#8b5cf6", "#14b8a6"
        ]
        
        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Orders",
                    "data": data,
                    "backgroundColor": colors[:len(data)],
                    "borderColor": "#1e293b",
                    "borderWidth": 1,
                    "borderRadius": 4,
                }
            ],
        }
    
    # ── Admin Actions ──
    actions = ['mark_as_paid', 'mark_as_unpaid']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
        self.message_user(request, f"{queryset.count()} orders marked as paid.")
    mark_as_paid.short_description = "✅ Mark selected orders as paid"
    
    def mark_as_unpaid(self, request, queryset):
        queryset.update(paid=False)
        self.message_user(request, f"{queryset.count()} orders marked as unpaid.")
    mark_as_unpaid.short_description = "❌ Mark selected orders as unpaid"










# from django.contrib import admin
# from admincharts.admin import AdminChartMixin
# from .models import Product, Order, OrderItem

# # Register Product
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'created_at')
#     search_fields = ('name', 'description')

# # Register OrderItem
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'product', 'quantity', 'price')

# # Register Order with Chart
# @admin.register(Order)
# class OrderAdmin(AdminChartMixin, admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'email', 'paid', 'created_at')
#     list_filter = ('paid', 'created_at')
#     search_fields = ('first_name', 'last_name', 'email')
    
#     # Chart settings
#     list_chart_title = "Orders Overview"
#     list_chart_type = "bar"  # 'bar', 'line', 'pie', 'doughnut'
    
#     def get_list_chart_data(self, queryset):
#         """Generate chart data"""
#         if not queryset.exists():
#             return {
#                 "labels": ["No Data"],
#                 "datasets": [{
#                     "label": "Orders",
#                     "data": [0],
#                     "backgroundColor": "#cccccc",
#                 }]
#             }
        
#         # Count orders by month
#         months = {}
#         for order in queryset:
#             month_key = order.created_at.strftime('%b %Y')
#             months[month_key] = months.get(month_key, 0) + 1
        
#         # Sort by date
#         import datetime
#         sorted_months = sorted(months.items(), key=lambda x: datetime.datetime.strptime(x[0], '%b %Y'))
        
#         labels = [item[0] for item in sorted_months]
#         data = [item[1] for item in sorted_months]
        
#         return {
#             "labels": labels,
#             "datasets": [
#                 {
#                     "label": "Orders",
#                     "data": data,
#                     "backgroundColor": [
#                         "#3498db", "#2ecc71", "#e74c3c", 
#                         "#f39c12", "#9b59b6", "#1abc9c",
#                         "#e67e22", "#34495e", "#95a5a6"
#                     ][:len(data)],
#                 }
#             ],
#         }