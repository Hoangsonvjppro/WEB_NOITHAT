from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from apps.products.models import Product
from apps.accounts.models import Customer

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user, membership_type='regular')
    cart, created = Cart.objects.get_or_create(customer=customer)
    return render(request, 'cart/cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user, membership_type='regular')
    cart, created = Cart.objects.get_or_create(customer=customer)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart')

def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart:cart')