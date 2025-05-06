from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from datetime import timedelta

from orders.models import Order, OrderItem
from inventory.models import InventoryRecord
from accounts.models import User

@login_required
def reports_dashboard(request):
    """Hiển thị trang tổng quan các báo cáo"""
    if not (request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    # Thống kê cơ bản
    total_orders = Order.objects.count()
    total_users = User.objects.filter(role=User.CUSTOMER).count()
    
    context = {
        'total_orders': total_orders,
        'total_users': total_users,
    }
    
    return render(request, 'reports/dashboard.html', context)

@login_required
def sales_report(request):
    """Hiển thị báo cáo doanh số"""
    if not (request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    # Mặc định xem báo cáo 30 ngày gần nhất
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # Lọc theo ngày nếu có
    date_range = request.GET.get('date_range', '30')
    if date_range == '7':
        start_date = end_date - timedelta(days=7)
    elif date_range == '90':
        start_date = end_date - timedelta(days=90)
    elif date_range == '365':
        start_date = end_date - timedelta(days=365)
    
    # Truy vấn dữ liệu
    orders = Order.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date,
        status__in=['completed', 'shipped']
    )
    
    context = {
        'orders': orders,
        'date_range': date_range,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'reports/sales_report.html', context)

@login_required
def inventory_report(request):
    """Hiển thị báo cáo tồn kho"""
    if not (request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    # Lấy thông tin tồn kho
    low_stock_items = InventoryRecord.objects.filter(quantity__lte=F('min_stock_level'))
    
    context = {
        'low_stock_items': low_stock_items,
    }
    
    return render(request, 'reports/inventory_report.html', context)

@login_required
def performance_report(request):
    """Hiển thị báo cáo hiệu suất"""
    if not (request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    # Mặc định xem báo cáo 30 ngày gần nhất
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # Truy vấn dữ liệu hiệu suất
    top_products = OrderItem.objects.filter(
        order__created_at__gte=start_date,
        order__created_at__lte=end_date,
        order__status__in=['completed', 'shipped']
    ).values('product__name').annotate(
        total_sales=Sum('quantity'),
        total_revenue=Sum(F('price') * F('quantity'))
    ).order_by('-total_sales')[:10]
    
    context = {
        'top_products': top_products,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'reports/performance_report.html', context)
