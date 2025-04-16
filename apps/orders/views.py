from django.shortcuts import render, redirect
from .models import Order, OrderItem
from apps.cart.models import Cart, CartItem
from apps.accounts.models import Customer

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user, membership_type='regular')
    cart = Cart.objects.get(customer=customer)
    if request.method == 'POST':
        total_amount = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            payment_method=request.POST.get('payment_method', 'Cash'),
        )
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )
            item.product.stock -= item.quantity
            item.product.save()
        cart.cartitem_set.all().delete()
        return redirect('orders:order_history')
    return render(request, 'orders/checkout.html', {'cart': cart})

def order_history(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user, membership_type='regular')
    orders = Order.objects.filter(customer=customer).order_by('-order_date')
    return render(request, 'orders/order_history.html', {'orders': orders})