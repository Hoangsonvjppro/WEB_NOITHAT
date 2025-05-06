from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, CustomerProfileForm
from .models import User, CustomerProfile
from orders.models import Order

def login_view(request):
    """View xử lý đăng nhập"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                messages.success(request, f'Xin chào, {user.get_full_name()}!')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """View xử lý đăng xuất"""
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công!')
    return redirect('home')

def register_view(request):
    """View xử lý đăng ký tài khoản"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                CustomerProfile.objects.create(user=user)
                login(request, user)
                messages.success(request, 'Đăng ký tài khoản thành công!')
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    """View hiển thị thông tin tài khoản"""
    # Lấy 5 đơn hàng gần nhất
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'user': request.user,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    """View xử lý cập nhật thông tin tài khoản"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        # Lấy hoặc tạo CustomerProfile nếu chưa có
        try:
            profile = request.user.customer_profile
        except CustomerProfile.DoesNotExist:
            profile = CustomerProfile(user=request.user)
        
        profile_form = CustomerProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Thông tin tài khoản đã được cập nhật!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        
        # Lấy hoặc tạo CustomerProfile nếu chưa có
        try:
            profile = request.user.customer_profile
        except CustomerProfile.DoesNotExist:
            profile = CustomerProfile(user=request.user)
            
        profile_form = CustomerProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def address_view(request):
    """View xử lý địa chỉ giao hàng"""
    try:
        profile = request.user.customer_profile
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Địa chỉ giao hàng đã được cập nhật!')
            return redirect('accounts:profile')
    else:
        form = CustomerProfileForm(instance=profile)
    
    return render(request, 'accounts/address.html', {'form': form})

@login_required
def orders_view(request):
    """View hiển thị lịch sử đơn hàng"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/orders.html', {'orders': orders})
