from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem


def _get_or_create_cart(request):
    """Helper function to get or create cart for user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Ensure session exists before trying to access session_key
        if not request.session.exists(request.session.session_key):
            request.session.create()
            
        session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    return cart


def cart_detail(request):
    """Display cart contents"""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add a product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        quantity = 1
    
    # Check if product is already in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Đã cập nhật số lượng "{product.name}" trong giỏ hàng!')
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        messages.success(request, f'Đã thêm "{product.name}" vào giỏ hàng!')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': cart.total_quantity,
            'message': f'Đã thêm "{product.name}" vào giỏ hàng!'
        })
        
    return redirect('cart:cart_detail')


@require_POST
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Check if the cart belongs to the user
    if request.user.is_authenticated and cart_item.cart.user != request.user:
        messages.error(request, 'Bạn không có quyền cập nhật mục này!')
        return redirect('cart:cart_detail')
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Giỏ hàng đã được cập nhật!')
    else:
        cart_item.delete()
        messages.success(request, 'Sản phẩm đã được xóa khỏi giỏ hàng!')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = _get_or_create_cart(request)
        return JsonResponse({
            'status': 'success',
            'cart_count': cart.total_quantity,
            'cart_total': cart.total_price,
            'item_total': cart_item.total_price if quantity > 0 else 0
        })
    
    return redirect('cart:cart_detail')


@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Check if the cart belongs to the user
    if request.user.is_authenticated and cart_item.cart.user != request.user:
        messages.error(request, 'Bạn không có quyền xóa mục này!')
        return redirect('cart:cart_detail')
    
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Đã xóa "{product_name}" khỏi giỏ hàng!')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = _get_or_create_cart(request)
        return JsonResponse({
            'status': 'success',
            'cart_count': cart.total_quantity,
            'cart_total': cart.total_price
        })
    
    return redirect('cart:cart_detail')


@require_POST
def clear_cart(request):
    """Clear all items from cart"""
    cart = _get_or_create_cart(request)
    cart.clear()
    messages.success(request, 'Giỏ hàng của bạn đã được xóa!')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': 0,
            'cart_total': 0
        })
    
    return redirect('cart:cart_detail')


def merge_carts(request):
    """Merge anonymous cart with user cart on login"""
    if request.user.is_authenticated and request.session.get('session_key'):
        try:
            # Get the anonymous cart
            anonymous_cart = Cart.objects.get(session_id=request.session.get('session_key'))
            
            # Get or create user cart
            user_cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Merge items
            for item in anonymous_cart.items.all():
                try:
                    # Check if product already in user cart
                    user_item = CartItem.objects.get(cart=user_cart, product=item.product)
                    user_item.quantity += item.quantity
                    user_item.save()
                except CartItem.DoesNotExist:
                    # Move item to user cart
                    item.cart = user_cart
                    item.save()
            
            # Delete anonymous cart
            anonymous_cart.delete()
            messages.success(request, 'Giỏ hàng của bạn đã được giữ lại từ phiên trước đó!')
            
        except Cart.DoesNotExist:
            pass
    
    return redirect('cart:cart_detail')
