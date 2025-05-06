from .models import Cart


def cart_count(request):
    """
    Context processor to get the cart item count for the current user
    """
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.total_quantity
        except Cart.DoesNotExist:
            pass
    elif hasattr(request, 'session'):
        session_id = request.session.session_key
        if session_id:
            try:
                cart = Cart.objects.get(session_id=session_id)
                count = cart.total_quantity
            except Cart.DoesNotExist:
                pass
    
    return {'cart_count': count} 