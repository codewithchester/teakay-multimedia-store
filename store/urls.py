from django.urls import path
from . import views
from .admin_dashboard import admin_dashboard
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('payment/verify/', views.payment_verify, name='payment_verify'),
    
    # Admin dashboard
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),


]











# from django.urls import path 
# from . import views
# urlpatterns = [
#      path('', views.product_list, name = 'product_list'),
#      path('product/<int:product_id>/', views.product_detail, name='product_detail'),
#      path('checkout/', views.checkout, name='checkout'),
#      path('order/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
# ]


# from django.urls import path 
# from . import views

# urlpatterns = [
#     path('', views.product_list, name='product_list'),
#     path('product/<int:product_id>/', views.product_detail, name='product_detail'),
#     path('checkout/', views.checkout, name='checkout'),
#     path('order/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    
#     # Paystack payment URLs
#     path('payment/verify/', views.payment_verify, name='payment_verify'),


# ]
