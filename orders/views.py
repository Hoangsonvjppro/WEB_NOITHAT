from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.http import HttpResponse
# from django.template.loader import render_to_string
# from xhtml2pdf import pisa
from django.conf import settings
import os

from .models import Order, OrderItem, Payment
from cart.models import Cart
from branches.models import Branch
from accounts.models import User
from products.models import Product

from .forms import CheckoutForm, PaymentForm


@login_required
def checkout(request):
    """Display checkout form and process order"""
    # Get user's cart
    try:
        cart = Cart.objects.get(user=request.user)
        if cart.items.count() == 0:
            messages.warning(request, 'Giỏ hàng của bạn đang trống. Vui lòng thêm sản phẩm vào giỏ hàng trước.')
            return redirect('cart:cart_detail')
    except Cart.DoesNotExist:
        messages.warning(request, 'Giỏ hàng của bạn đang trống. Vui lòng thêm sản phẩm vào giỏ hàng trước.')
        return redirect('cart:cart_detail')
    
    # Initialize form with user data if available
    initial_data = {}
    if hasattr(request.user, 'customer_profile'):
        profile = request.user.customer_profile
        initial_data = {
            'shipping_name': request.user.get_full_name(),
            'shipping_email': request.user.email,
            'shipping_phone': request.user.phone_number,
            'shipping_address': profile.address,
        }
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Get the nearest branch (in a real app, you would determine this based on location)
            branch = Branch.objects.filter(is_active=True).first()
            
            # Create the order
            order = Order(
                user=request.user,
                branch=branch,
                shipping_name=form.cleaned_data['shipping_name'],
                shipping_email=form.cleaned_data['shipping_email'],
                shipping_phone=form.cleaned_data['shipping_phone'],
                shipping_address=form.cleaned_data['shipping_address'],
                notes=form.cleaned_data['notes'],
                payment_method=form.cleaned_data['payment_method'],
                shipping_fee=form.cleaned_data.get('shipping_fee', 0),
                total_amount=cart.total_price + form.cleaned_data.get('shipping_fee', 0),
            )
            order.save()
            
            # Create order items from cart items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    quantity=cart_item.quantity,
                    price=cart_item.product.current_price,
                    total_price=cart_item.total_price
                )
            
            # Clear the cart after creating the order
            cart.clear()
            
            # Store order ID in session
            request.session['order_id'] = order.id
            
            # Redirect to payment if not COD
            if order.payment_method == Order.PAYMENT_METHOD_COD:
                order.payment_status = Order.PAYMENT_PENDING
                order.save()
                messages.success(request, 'Đơn hàng của bạn đã được đặt thành công. Cảm ơn bạn đã mua hàng!')
                return redirect('orders:order_complete')
            else:
                return redirect('orders:payment')
    else:
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def payment(request):
    """Process payment for an order"""
    # Get the order from session
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, 'Không tìm thấy đơn hàng. Vui lòng thử lại.')
        return redirect('cart:cart_detail')
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process payment (in a real app, you would integrate with payment gateway)
            payment = Payment(
                order=order,
                amount=order.total_amount,
                payment_method=order.payment_method,
                transaction_id=form.cleaned_data.get('transaction_id', ''),
                is_successful=True,  # In real app, this would be set by payment gateway callback
                notes=form.cleaned_data.get('notes', '')
            )
            payment.save()
            
            # Update order status
            order.payment_status = Order.PAYMENT_PAID
            order.status = Order.STATUS_PROCESSING
            order.save()
            
            messages.success(request, 'Thanh toán thành công! Đơn hàng của bạn đang được xử lý.')
            return redirect('orders:order_complete')
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'order': order,
    }
    return render(request, 'orders/payment.html', context)


@login_required
def order_complete(request):
    """Display order complete page"""
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('products:product_list')
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Clear the order_id from session
    if 'order_id' in request.session:
        del request.session['order_id']
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_complete.html', context)


@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user is authorized to view this order
    if not (order.user == request.user or 
           (request.user.is_staff and request.user.role in 
            [User.BUSINESS_OWNER, User.BRANCH_MANAGER, User.SALES_STAFF])):
        raise PermissionDenied
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_history(request):
    """Display order history for a user"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)


@login_required
def generate_invoice(request, order_id):
    """Generate PDF invoice for an order"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user is authorized to view this order
    if not (order.user == request.user or 
           (request.user.is_staff and request.user.role in 
            [User.BUSINESS_OWNER, User.BRANCH_MANAGER, User.SALES_STAFF])):
        raise PermissionDenied
    
    # Return a simple text response instead of PDF for now
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.txt"'
    
    # Write invoice details to the response
    content = f"""
    INVOICE #{order.order_number}
    Date: {order.created_at.strftime('%d/%m/%Y')}
    
    CUSTOMER INFORMATION
    Name: {order.shipping_name}
    Email: {order.shipping_email}
    Phone: {order.shipping_phone}
    Address: {order.shipping_address}
    
    ORDER DETAILS
    Status: {order.get_status_display()}
    Payment Method: {order.get_payment_method_display()}
    Payment Status: {order.get_payment_status_display()}
    
    ITEMS:
    """
    
    for item in order.items.all():
        content += f"\n{item.product_name} x {item.quantity} = {item.total_price} VND"
    
    content += f"""
    
    Subtotal: {order.subtotal} VND
    Shipping Fee: {order.shipping_fee} VND
    Total: {order.total_amount} VND
    
    Thank you for your order!
    """
    
    response.write(content)
    return response
