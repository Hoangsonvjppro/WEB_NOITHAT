from .models import Cart

def cart_info(request):
    context = {'cart_item_count': 0}
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            context['cart_item_count'] = cart.cartitem_set.count()
        except Cart.DoesNotExist:
            pass
    return context
