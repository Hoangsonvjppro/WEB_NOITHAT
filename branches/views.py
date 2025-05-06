from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Branch

def branch_list(request):
    """Hiển thị danh sách các chi nhánh"""
    branches = Branch.objects.filter(is_active=True)
    context = {
        'branches': branches,
    }
    return render(request, 'branches/branch_list.html', context)

def branch_detail(request, pk):
    """Hiển thị thông tin chi tiết chi nhánh"""
    branch = get_object_or_404(Branch, pk=pk, is_active=True)
    context = {
        'branch': branch,
    }
    return render(request, 'branches/branch_detail.html', context)
