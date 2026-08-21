# from django.shortcuts import render, redirect, get_object_or_404
# from store.models import Product
# from django.contrib import messages


# def cart_summary(request):
#     """Show all items in the cart"""
#     cart = request.session.get('cart', {})
    
#     cart_items = []
#     total_price = 0
    
#     for product_id, quantity in cart.items():
#         product = Product.objects.get(id=int(product_id))
#         item_total = product.price * quantity
#         total_price += item_total
        
#         cart_items.append({
#             'product': product,
#             'quantity': quantity,
#             'item_total': item_total,
#         })
    
#     return render(request, 'cart/cart_summary.html', {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     })


# def cart_add(request, product_id):
#     """Add a product to the cart"""
#     cart = request.session.get('cart', {})
    
#     product_id = str(product_id)
    
#     if product_id in cart:
#         cart[product_id] += 1
#     else:
#         cart[product_id] = 1
    
#     request.session['cart'] = cart
#     messages.success(request, 'Product added to cart!')
    
#     return redirect('cart_summary')


# def cart_remove(request, product_id):
#     """Remove a product from the cart"""
#     cart = request.session.get('cart', {})
    
#     product_id = str(product_id)
    
#     if product_id in cart:
#         del cart[product_id]
#         request.session['cart'] = cart
#         messages.success(request, 'Product removed from cart!')
    
#     return redirect('cart_summary')


# def cart_update(request, product_id):
#     """Update quantity of a product in cart"""
#     cart = request.session.get('cart', {})
    
#     product_id = str(product_id)
    
#     if request.method == 'POST':
#         quantity = int(request.POST.get('quantity', 1))
        
#         if quantity > 0:
#             cart[product_id] = quantity
#         else:
#             del cart[product_id]
        
#         request.session['cart'] = cart
    
#     return redirect('cart_summary')






from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.contrib import messages


def cart_summary(request):
    """Show all items in the cart"""
    cart = request.session.get('cart', {})
    
    cart_items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            total_price += item_total
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
        except Product.DoesNotExist:
            # Remove stale item from cart
            del cart[product_id]
            request.session['cart'] = cart
    
    # Get cart count for badge
    cart_count = sum(cart.values())
    
    return render(request, 'cart/cart_summary.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,  # Added this
    })


def cart_add(request, product_id):
    """Add a product to the cart"""
    cart = request.session.get('cart', {})
    
    product_id = str(product_id)
    
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    
    request.session['cart'] = cart
    messages.success(request, 'Product added to cart!')
    
    return redirect('cart_summary')


def cart_remove(request, product_id):
    """Remove a product from the cart"""
    cart = request.session.get('cart', {})
    
    product_id = str(product_id)
    
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, 'Product removed from cart!')
    
    return redirect('cart_summary')


def cart_update(request, product_id):
    """Update quantity of a product in cart"""
    cart = request.session.get('cart', {})
    
    product_id = str(product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart[product_id] = quantity
        else:
            del cart[product_id]
        
        request.session['cart'] = cart
    
    return redirect('cart_summary')