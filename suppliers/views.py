from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Supplier

@login_required
def supplier_list(request):
    """Hiển thị danh sách nhà cung cấp"""
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    suppliers = Supplier.objects.all()
    context = {
        'suppliers': suppliers
    }
    return render(request, 'suppliers/supplier_list.html', context)

@login_required
def supplier_detail(request, pk):
    """Hiển thị thông tin chi tiết nhà cung cấp"""
    if not (request.user.is_inventory_manager or request.user.is_branch_manager or request.user.is_business_owner):
        messages.error(request, 'Bạn không có quyền truy cập vào trang này.')
        return redirect('home')
    
    supplier = get_object_or_404(Supplier, pk=pk)
    context = {
        'supplier': supplier
    }
    return render(request, 'suppliers/supplier_detail.html', context)
