from django.contrib import admin
from .models import Product, Order, OrderItem


# ─── CUSTOM ADMIN SITE ───
admin.site.site_header = "🛍️ Teakay Store Admin"
admin.site.site_title = "Teakay Store"
admin.site.index_title = "Welcome to Teakay Store Admin"


# ─── PRODUCT ADMIN ───
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    
    # Group fields for better UI
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'price', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# ─── ORDER ITEM ADMIN ───
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total')
    list_filter = ('order',)
    search_fields = ('product__name', 'order__email')
    
    def total(self, obj):
        return obj.price * obj.quantity
    total.short_description = "Total"


# ─── ORDER ADMIN ───
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'email', 'paid', 'created_at')
    list_filter = ('paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-created_at',)
    exclude = ('created_at',)

    # Group fields for better UI
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
    
    
    # Custom method
    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = "Customer"
    
    # Bulk actions
    actions = ['mark_as_paid', 'mark_as_unpaid']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
        self.message_user(request, f"{queryset.count()} orders marked as paid.")
    mark_as_paid.short_description = "✅ Mark as paid"
    
    def mark_as_unpaid(self, request, queryset):
        queryset.update(paid=False)
        self.message_user(request, f"{queryset.count()} orders marked as unpaid.")
    mark_as_unpaid.short_description = "❌ Mark as unpaid"