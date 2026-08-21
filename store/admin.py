from django.contrib import admin
from .models import Product, Order, OrderItem


# ─── PRODUCT ADMIN ───
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)


# ─── ORDER ITEM ADMIN ───
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order',)
    search_fields = ('product__name', 'order__email')


# ─── ORDER ADMIN ───
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'paid', 'created_at')
    list_filter = ('paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-created_at',)
    
    # Bulk actions
    actions = ['mark_as_paid', 'mark_as_unpaid']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
        self.message_user(request, f"{queryset.count()} orders marked as paid.")
    mark_as_paid.short_description = "✅ Mark selected orders as paid"
    
    def mark_as_unpaid(self, request, queryset):
        queryset.update(paid=False)
        self.message_user(request, f"{queryset.count()} orders marked as unpaid.")
    mark_as_unpaid.short_description = "❌ Mark selected orders as unpaid"