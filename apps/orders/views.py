from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    # Tính tổng giá cho từng OrderItem
    for order in orders:
        for item in order.orderitem_set.all():
            item.total = item.quantity * item.price  # Thêm thuộc tính total
    return render(request, 'orders/order_history.html', {'orders': orders})