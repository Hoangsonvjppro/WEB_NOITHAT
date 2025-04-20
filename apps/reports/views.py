from django.shortcuts import render
from apps.orders.models import Order
from django.db.models import Sum
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def sales_report(request):
    """
    Hiển thị báo cáo doanh thu dựa trên khoảng thời gian được chọn.
    """
    start_date = request.GET.get('start_date', datetime.now().strftime('%Y-%m-01'))
    end_date = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))

    try:
        # Chuyển đổi ngày để tránh lỗi định dạng
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        start_date = datetime.now().replace(day=1).date()
        end_date = datetime.now().date()

    orders = Order.objects.filter(order_date__range=[start_date, end_date])
    total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

    return render(request, 'reports/sales_report.html', {
        'orders': orders,
        'total_revenue': total_revenue,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    })