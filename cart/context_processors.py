def cart_count(request):
    """
    Context processor to add cart item count to all templates.
    """
    cart = request.session.get('cart', {})
    count = sum(cart.values())  # Total quantity of all items
    return {'cart_count': count}