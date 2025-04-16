from django.shortcuts import render, redirect
from apps.orders.models import Order
from django.db.models import Sum
from datetime import datetime

def sales_report(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('accounts:login')
    start_date = request.GET.get('start_date', datetime.now().strftime('%Y-%m-01'))
    end_date = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    orders = Order.objects.filter(order_date__range=[start_date, end_date])
    total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    return render(request, 'reports/sales_report.html', {
        'orders': orders,
        'total_revenue': total_revenue,
        'start_date': start_date,
        'end_date': end_date,
    })