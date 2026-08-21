# # def checkout(request):
# #     """Handle order processing with Paystack"""
# #     cart = request.session.get('cart', {})
    
# #     # If cart is empty, go back to store
# #     if not cart:
# #         messages.error(request, 'Your cart is empty!')
# #         return redirect('product_list')
    
# #     # Calculate total
# #     total = 0
# #     cart_items = []
# #     for product_id, quantity in cart.items():
# #         try:
# #             product = Product.objects.get(id=int(product_id))
# #             item_total = product.price * quantity
# #             total += item_total
# #             cart_items.append({
# #                 'product': product,
# #                 'quantity': quantity,
# #                 'item_total': item_total
# #             })
# #         except Product.DoesNotExist:
# #             messages.warning(request, f'Product {product_id} no longer exists. Please remove it from your cart.')
# #             return redirect('cart_summary')
    
# #     if request.method == 'POST':
# #         # Get customer info from the form
# #         first_name = request.POST.get('first_name')
# #         last_name = request.POST.get('last_name')
# #         email = request.POST.get('email')
# #         address = request.POST.get('address')
# #         phone = request.POST.get('phone')
        
# #         # Validate required fields
# #         if not all([first_name, last_name, email, address, phone]):
# #             messages.error(request, 'Please fill in all required fields.')
# #             return render(request, 'store/checkout.html', {
# #                 'cart_items': cart_items,
# #                 'total': total
# #             })
        
# #         # Create the order (not paid yet)
# #         order = Order.objects.create(
# #             first_name=first_name,
# #             last_name=last_name,
# #             email=email,
# #             address=address,
# #             phone=phone,
# #             paid=False,
# #         )
        
# #         # Add each cart item to the order
# #         for product_id, quantity in cart.items():
# #             try:
# #                 product = Product.objects.get(id=int(product_id))
# #                 OrderItem.objects.create(
# #                     order=order,
# #                     product=product,
# #                     price=product.price,
# #                     quantity=quantity,
# #                 )
# #             except Product.DoesNotExist:
# #                 continue
        
# #         # Generate transaction reference
# #         reference = generate_reference()
        
# #         # Build callback URL
# #         base_url = request.build_absolute_uri('/')[:-1]
# #         callback_url = f"{base_url}{reverse('payment_verify')}"
        
# #         # Initialize Paystack payment
# #         try:
# #             response = initialize_payment(
# #                 email=email,
# #                 amount=total,
# #                 reference=reference,
# #                 callback_url=callback_url,
# #                 metadata={
# #                     'order_id': order.id,
# #                     'first_name': first_name,
# #                     'last_name': last_name,
# #                     'cart': cart
# #                 }
# #             )
            
# #             if response['status']:
# #                 # Store reference and order ID in session
# #                 request.session['transaction_reference'] = reference
# #                 request.session['pending_order_id'] = order.id
                
# #                 # Get the authorization URL
# #                 authorization_url = response['data']['authorization_url']
                
# #                 # Clear the cart (we'll keep the order)
# #                 request.session['cart'] = {}
                
# #                 # Redirect to Paystack payment page
# #                 return redirect(authorization_url)
# #             else:
# #                 messages.error(request, f'Payment initialization failed: {response.get("message", "Unknown error")}')
# #                 order.delete()
# #                 return render(request, 'store/checkout.html', {
# #                     'cart_items': cart_items,
# #                     'total': total
# #                 })
                
# #         except Exception as e:
# #             messages.error(request, f'Payment error: {str(e)}')
# #             order.delete()
# #             return render(request, 'store/checkout.html', {
# #                 'cart_items': cart_items,
# #                 'total': total
# #             })
    
# #     # GET request - show checkout form
# #     context = {
# #         'cart_items': cart_items,
# #         'total': total,
# #         'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
# #     }
# #     return render(request, 'store/checkout.html', context)




# # #payment verification view

# # def payment_verify(request):
# #     """Verify Paystack payment after redirect"""
# #     reference = request.GET.get('reference')
    
# #     if not reference:
# #         # Also check session
# #         reference = request.session.get('transaction_reference')
    
# #     if not reference:
# #         messages.error(request, 'Payment reference not found.')
# #         return redirect('product_list')
    
# #     try:
# #         # Verify payment with Paystack
# #         response = verify_payment(reference)
        
# #         if response['status']:
# #             data = response['data']
            
# #             # Check if payment was successful
# #             if data['status'] == 'success':
# #                 # Get the order from metadata
# #                 order_id = data['metadata']['order_id']
# #                 order = Order.objects.get(id=order_id)
                
# #                 # Mark order as paid
# #                 order.paid = True
# #                 order.save()
                
# #                 # Clear session
# #                 request.session.pop('transaction_reference', None)
# #                 request.session.pop('pending_order_id', None)
                
# #                 messages.success(request, f'Payment successful! Order #{order.id} is confirmed.')
# #                 return redirect('order_confirmation', order_id=order.id)
# #             else:
# #                 messages.error(request, f'Payment not successful. Status: {data["status"]}')
# #                 # Delete the order if payment failed
# #                 order_id = data.get('metadata', {}).get('order_id')
# #                 if order_id:
# #                     try:
# #                         order = Order.objects.get(id=order_id)
# #                         order.delete()
# #                     except Order.DoesNotExist:
# #                         pass
# #                 return redirect('checkout')
# #         else:
# #             messages.error(request, f'Payment verification failed: {response.get("message", "Unknown error")}')
# #             # Try to clean up
# #             order_id = request.session.get('pending_order_id')
# #             if order_id:
# #                 try:
# #                     order = Order.objects.get(id=order_id)
# #                     order.delete()
# #                 except Order.DoesNotExist:
# #                     pass
# #             request.session.pop('transaction_reference', None)
# #             request.session.pop('pending_order_id', None)
# #             return redirect('checkout')
            
# #     except Order.DoesNotExist:
# #         messages.error(request, 'Order not found.')
# #         return redirect('product_list')
# #     except Exception as e:
# #         messages.error(request, f'Verification error: {str(e)}')
# #         return redirect('checkout')























# # # from django.shortcuts import render, get_object_or_404, redirect
# # # from .models import Product, Order, OrderItem
# # # from django.contrib import messages

# # # def product_list(request):
# # #     products = Product.objects.all()
# # #     return render(request, 'store/product_list.html', {'products': products})


# # # def product_detail(request, product_id):
# # #     product = Product.objects.get(id=product_id)
# # #     return render(request, 'store/product_detail.html', {'product': product})


# # # def checkout(request):
# # #     """Handle order processing"""
# # #     cart = request.session.get('cart', {})
    
# # #     # If cart is empty, go back to store
# # #     if not cart:
# # #         messages.error(request, 'Your cart is empty!')
# # #         return redirect('product_list')
    
# # #     if request.method == 'POST':
# # #         # Get customer info from the form
# # #         first_name = request.POST.get('first_name')
# # #         last_name = request.POST.get('last_name')
# # #         email = request.POST.get('email')
# # #         address = request.POST.get('address')
# # #         phone = request.POST.get('phone')
        
# # #         # Create the order
# # #         order = Order.objects.create(
# # #             first_name=first_name,
# # #             last_name=last_name,
# # #             email=email,
# # #             address=address,
# # #             phone=phone,
# # #         )
        
# # #         # Add each cart item to the order
# # #         for product_id, quantity in cart.items():
# # #             product = Product.objects.get(id=int(product_id))
# # #             OrderItem.objects.create(
# # #                 order=order,
# # #                 product=product,
# # #                 price=product.price,
# # #                 quantity=quantity,
# # #             )
        
# # #         # Clear the cart
# # #         request.session['cart'] = {}
        
# # #         messages.success(request, f'Order #{order.id} placed successfully! Thank you for your purchase.')
# # #         return redirect('order_confirmation', order_id=order.id)
    
# # #     return render(request, 'store/checkout.html', {'cart': cart})


# # # def order_confirmation(request, order_id):
# # #     """Show order confirmation page"""
# # #     order = get_object_or_404(Order, id=order_id)
# # #     return render(request, 'store/order_confirmation.html', {'order': order})

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from django.urls import reverse
# from django.conf import settings
# from .models import Product, Order, OrderItem

# # Paystack imports
# try:
#     from .paystack_utils import initialize_payment, verify_payment, generate_reference
#     PAYSTACK_AVAILABLE = True
# except ImportError:
#     PAYSTACK_AVAILABLE = False


# def product_list(request):
#     """Display all products"""
#     products = Product.objects.all()
#     return render(request, 'store/product_list.html', {'products': products})


# def product_detail(request, product_id):
#     """Display a single product"""
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'store/product_detail.html', {'product': product})


# def checkout(request):
#     """Handle order processing with Paystack"""
#     cart = request.session.get('cart', {})
    
#     # If cart is empty, go back to store
#     if not cart:
#         messages.error(request, 'Your cart is empty!')
#         return redirect('product_list')
    
#     # Calculate total
#     total = 0
#     cart_items = []
#     for product_id, quantity in cart.items():
#         try:
#             product = Product.objects.get(id=int(product_id))
#             item_total = product.price * quantity
#             total += item_total
#             cart_items.append({
#                 'product': product,
#                 'quantity': quantity,
#                 'item_total': item_total
#             })
#         except Product.DoesNotExist:
#             messages.warning(request, f'Product no longer exists. Please remove it from your cart.')
#             return redirect('cart_summary')
    
#     if request.method == 'POST':
#         # Get customer info from the form
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
        
#         # Validate required fields
#         if not all([first_name, last_name, email, address, phone]):
#             messages.error(request, 'Please fill in all required fields.')
#             return render(request, 'store/checkout.html', {
#                 'cart_items': cart_items,
#                 'total': total
#             })
        
#         # Create the order (not paid yet)
#         order = Order.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             address=address,
#             phone=phone,
#             paid=False,
#         )
        
#         # Add each cart item to the order
#         for product_id, quantity in cart.items():
#             try:
#                 product = Product.objects.get(id=int(product_id))
#                 OrderItem.objects.create(
#                     order=order,
#                     product=product,
#                     price=product.price,
#                     quantity=quantity,
#                 )
#             except Product.DoesNotExist:
#                 continue
        
#         # Check if Paystack is available
#         if not PAYSTACK_AVAILABLE:
#             messages.warning(request, 'Payment system not configured yet. Order created but not paid.')
#             request.session['cart'] = {}
#             return redirect('order_confirmation', order_id=order.id)
        
#         # Generate transaction reference
#         reference = generate_reference()
        
#         # Build callback URL
#         base_url = request.build_absolute_uri('/')[:-1]
#         callback_url = f"{base_url}{reverse('payment_verify')}"
        
#         # Initialize Paystack payment
#         try:
#             response = initialize_payment(
#                 email=email,
#                 amount=total,
#                 reference=reference,
#                 callback_url=callback_url,
#                 metadata={
#                     'order_id': order.id,
#                     'first_name': first_name,
#                     'last_name': last_name,
#                     'cart': cart
#                 }
#             )
            
#             if response['status']:
#                 # Store reference and order ID in session
#                 request.session['transaction_reference'] = reference
#                 request.session['pending_order_id'] = order.id
                
#                 # Get the authorization URL
#                 authorization_url = response['data']['authorization_url']
                
#                 # Clear the cart (we'll keep the order)
#                 request.session['cart'] = {}
                
#                 # Redirect to Paystack payment page
#                 return redirect(authorization_url)
#             else:
#                 messages.error(request, f'Payment initialization failed: {response.get("message", "Unknown error")}')
#                 order.delete()
#                 return render(request, 'store/checkout.html', {
#                     'cart_items': cart_items,
#                     'total': total
#                 })
                
#         except Exception as e:
#             messages.error(request, f'Payment error: {str(e)}')
#             order.delete()
#             return render(request, 'store/checkout.html', {
#                 'cart_items': cart_items,
#                 'total': total
#             })
    
#     # GET request - show checkout form
#     context = {
#         'cart_items': cart_items,
#         'total': total,
#         'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY if hasattr(settings, 'PAYSTACK_PUBLIC_KEY') else '',
#     }
#     return render(request, 'store/checkout.html', context)


# def payment_verify(request):
#     """Verify Paystack payment after redirect"""
#     reference = request.GET.get('reference')
    
#     if not reference:
#         # Also check session
#         reference = request.session.get('transaction_reference')
    
#     if not reference:
#         messages.error(request, 'Payment reference not found.')
#         return redirect('product_list')
    
#     try:
#         # Verify payment with Paystack
#         response = verify_payment(reference)
        
#         if response['status']:
#             data = response['data']
            
#             # Check if payment was successful
#             if data['status'] == 'success':
#                 # Get the order from metadata
#                 order_id = data['metadata']['order_id']
#                 order = Order.objects.get(id=order_id)
                
#                 # Mark order as paid
#                 order.paid = True
#                 order.save()
                
#                 # Clear session
#                 request.session.pop('transaction_reference', None)
#                 request.session.pop('pending_order_id', None)
                
#                 messages.success(request, f'Payment successful! Order #{order.id} is confirmed.')
#                 return redirect('order_confirmation', order_id=order.id)
#             else:
#                 messages.error(request, f'Payment not successful. Status: {data["status"]}')
#                 # Delete the order if payment failed
#                 order_id = data.get('metadata', {}).get('order_id')
#                 if order_id:
#                     try:
#                         order = Order.objects.get(id=order_id)
#                         order.delete()
#                     except Order.DoesNotExist:
#                         pass
#                 return redirect('checkout')
#         else:
#             messages.error(request, f'Payment verification failed: {response.get("message", "Unknown error")}')
#             # Try to clean up
#             order_id = request.session.get('pending_order_id')
#             if order_id:
#                 try:
#                     order = Order.objects.get(id=order_id)
#                     order.delete()
#                 except Order.DoesNotExist:
#                     pass
#             request.session.pop('transaction_reference', None)
#             request.session.pop('pending_order_id', None)
#             return redirect('checkout')
            
#     except Order.DoesNotExist:
#         messages.error(request, 'Order not found.')
#         return redirect('product_list')
#     except Exception as e:
#         messages.error(request, f'Verification error: {str(e)}')
#         return redirect('checkout')


# def order_confirmation(request, order_id):
#     """Show order confirmation page"""
#     order = get_object_or_404(Order, id=order_id)
#     return render(request, 'store/order_confirmation.html', {'order': order})








from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from .models import Product, Order, OrderItem

# Paystack imports
try:
    from .paystack_utils import initialize_payment, verify_payment, generate_reference
    PAYSTACK_AVAILABLE = True
except ImportError:
    PAYSTACK_AVAILABLE = False


def product_list(request):
    """Display all products"""
    products = Product.objects.all()
    
    # Get cart count for badge
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'cart_count': cart_count,  # Added this
    })


def product_detail(request, product_id):
    """Display a single product"""
    product = get_object_or_404(Product, id=product_id)
    
    # Get cart count for badge
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'cart_count': cart_count,  # Added this
    })


def checkout(request):
    """Handle order processing with Paystack"""
    cart = request.session.get('cart', {})
    
    # If cart is empty, go back to store
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('product_list')
    
    # Calculate total
    total = 0
    cart_items = []
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
        except Product.DoesNotExist:
            messages.warning(request, f'Product no longer exists. Please remove it from your cart.')
            return redirect('cart_summary')
    
    # Get cart count for badge
    cart_count = sum(cart.values())
    
    if request.method == 'POST':
        # Get customer info from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        # Validate required fields
        if not all([first_name, last_name, email, address, phone]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'cart_count': cart_count,  # Added this
            })
        
        # Create the order (not paid yet)
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone=phone,
            paid=False,
        )
        
        # Add each cart item to the order
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=quantity,
                )
            except Product.DoesNotExist:
                continue
        
        # Check if Paystack is available
        if not PAYSTACK_AVAILABLE:
            messages.warning(request, 'Payment system not configured yet. Order created but not paid.')
            request.session['cart'] = {}
            return redirect('order_confirmation', order_id=order.id)
        
        # Generate transaction reference
        reference = generate_reference()
        
        # Build callback URL
        base_url = request.build_absolute_uri('/')[:-1]
        callback_url = f"{base_url}{reverse('payment_verify')}"
        
        # Initialize Paystack payment
        try:
            response = initialize_payment(
                email=email,
                amount=total,
                reference=reference,
                callback_url=callback_url,
                metadata={
                    'order_id': order.id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'cart': cart
                }
            )
            
            if response['status']:
                # Store reference and order ID in session
                request.session['transaction_reference'] = reference
                request.session['pending_order_id'] = order.id
                
                # Get the authorization URL
                authorization_url = response['data']['authorization_url']
                
                # Clear the cart (we'll keep the order)
                request.session['cart'] = {}
                
                # Redirect to Paystack payment page
                return redirect(authorization_url)
            else:
                messages.error(request, f'Payment initialization failed: {response.get("message", "Unknown error")}')
                order.delete()
                return render(request, 'store/checkout.html', {
                    'cart_items': cart_items,
                    'total': total,
                    'cart_count': cart_count,  # Added this
                })
                
        except Exception as e:
            messages.error(request, f'Payment error: {str(e)}')
            order.delete()
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'cart_count': cart_count,  # Added this
            })
    
    # GET request - show checkout form
    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count,  # Added this
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY if hasattr(settings, 'PAYSTACK_PUBLIC_KEY') else '',
    }
    return render(request, 'store/checkout.html', context)


def payment_verify(request):
    """Verify Paystack payment after redirect"""
    reference = request.GET.get('reference')
    
    if not reference:
        # Also check session
        reference = request.session.get('transaction_reference')
    
    if not reference:
        messages.error(request, 'Payment reference not found.')
        return redirect('product_list')
    
    try:
        # Verify payment with Paystack
        response = verify_payment(reference)
        
        if response['status']:
            data = response['data']
            
            # Check if payment was successful
            if data['status'] == 'success':
                # Get the order from metadata
                order_id = data['metadata']['order_id']
                order = Order.objects.get(id=order_id)
                
                # Mark order as paid
                order.paid = True
                order.save()
                
                # Clear session
                request.session.pop('transaction_reference', None)
                request.session.pop('pending_order_id', None)
                
                messages.success(request, f'Payment successful! Order #{order.id} is confirmed.')
                return redirect('order_confirmation', order_id=order.id)
            else:
                messages.error(request, f'Payment not successful. Status: {data["status"]}')
                # Delete the order if payment failed
                order_id = data.get('metadata', {}).get('order_id')
                if order_id:
                    try:
                        order = Order.objects.get(id=order_id)
                        order.delete()
                    except Order.DoesNotExist:
                        pass
                return redirect('checkout')
        else:
            messages.error(request, f'Payment verification failed: {response.get("message", "Unknown error")}')
            # Try to clean up
            order_id = request.session.get('pending_order_id')
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    order.delete()
                except Order.DoesNotExist:
                    pass
            request.session.pop('transaction_reference', None)
            request.session.pop('pending_order_id', None)
            return redirect('checkout')
            
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('product_list')
    except Exception as e:
        messages.error(request, f'Verification error: {str(e)}')
        return redirect('checkout')


def order_confirmation(request, order_id):
    """Show order confirmation page"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})