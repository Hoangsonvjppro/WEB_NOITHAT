from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F, Q
from django.db import transaction

from .models import Warehouse, InventoryRecord, StockMovement
from products.models import Product

@login_required
def inventory_dashboard(request):
    """Hiển thị trang tổng quan kho hàng"""
    # Chỉ cho phép người dùng có quyền quản lý kho truy cập
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    warehouses = Warehouse.objects.all()
    low_stock_items = InventoryRecord.objects.filter(quantity__lte=F('min_stock_level'))
    recent_movements = StockMovement.objects.all().order_by('-created_at')[:10]
    
    context = {
        'warehouses': warehouses,
        'low_stock_items': low_stock_items,
        'recent_movements': recent_movements,
    }
    
    return render(request, 'inventory/dashboard.html', context)

@login_required
def warehouse_list(request):
    """Hiển thị danh sách kho hàng"""
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    warehouses = Warehouse.objects.all()
    
    context = {
        'warehouses': warehouses,
    }
    
    return render(request, 'inventory/warehouse_list.html', context)

@login_required
def warehouse_detail(request, pk):
    """Hiển thị thông tin chi tiết kho hàng"""
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    warehouse = get_object_or_404(Warehouse, pk=pk)
    inventory_records = InventoryRecord.objects.filter(warehouse=warehouse)
    
    context = {
        'warehouse': warehouse,
        'inventory_records': inventory_records,
    }
    
    return render(request, 'inventory/warehouse_detail.html', context)

@login_required
def stock_movement_list(request):
    """Hiển thị danh sách chuyển kho"""
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    movements = StockMovement.objects.all().order_by('-created_at')
    
    context = {
        'movements': movements,
    }
    
    return render(request, 'inventory/stock_movement_list.html', context)

@login_required
def stock_movement_create(request):
    """Tạo phiếu chuyển kho mới"""
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    # Xử lý form tạo phiếu chuyển kho
    # (phần này sẽ triển khai sau khi tạo form)
    
    context = {
        'warehouses': Warehouse.objects.all(),
        'products': Product.objects.all(),
    }
    
    return render(request, 'inventory/stock_movement_create.html', context)

@login_required
def inventory_reports(request):
    """Hiển thị báo cáo tồn kho"""
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    warehouse_id = request.GET.get('warehouse', None)
    
    if warehouse_id:
        inventory_records = InventoryRecord.objects.filter(warehouse_id=warehouse_id)
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    else:
        inventory_records = InventoryRecord.objects.all()
        warehouse = None
    
    warehouses = Warehouse.objects.all()
    
    context = {
        'inventory_records': inventory_records,
        'warehouses': warehouses,
        'selected_warehouse': warehouse,
    }
    
    return render(request, 'inventory/reports.html', context)
