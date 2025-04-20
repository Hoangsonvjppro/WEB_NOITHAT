from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem
from apps.products.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "Vui lòng đăng nhập để xem giỏ hàng.")
        return redirect('accounts:login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')

        if action == 'update':
            quantity = int(request.POST.get('quantity', 1))
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, "Đã cập nhật số lượng.")
            else:
                cart_item.delete()
                messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")

        elif action == 'remove':
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            cart_item.delete()
            messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")

        return redirect('cart:cart')

    # Tính tổng giá cho từng CartItem
    for item in cart_items:
        item.total = item.quantity * item.product.price
    total_price = sum(item.total for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.")
        return redirect('accounts:login')

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, "Đã thêm sản phẩm vào giỏ hàng.")
    return redirect('products:product_list')

@login_required
def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, "Vui lòng đăng nhập để thanh toán.")
        return redirect('accounts:login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    if not cart_items:
        messages.error(request, "Giỏ hàng trống. Vui lòng thêm sản phẩm trước khi thanh toán.")
        return redirect('products:product_list')

    # Trước khi tạo đơn hàng
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f"Sản phẩm {item.product.name} không đủ số lượng trong kho.")
            return redirect('cart:cart')

    # Tạo đơn hàng
    from apps.orders.models import Order, OrderItem
    order = Order.objects.create(user=request.user,
                                 total_price=sum(item.product.price * item.quantity for item in cart_items))
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        total_price = sum(item.total_price for item in cart_items)

    # Xóa giỏ hàng sau khi thanh toán
    cart_items.delete()
    messages.success(request, "Đơn hàng đã được tạo thành công!")
    return redirect('orders:order_history')