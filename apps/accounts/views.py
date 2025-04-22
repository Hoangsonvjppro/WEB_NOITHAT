from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Customer
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Sử dụng get_or_create để tránh lỗi trùng lặp
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={'membership_type': 'regular'}
            )
            login(request, user)
            return redirect('products:product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('products:product_list')

@login_required
def profile_view(request):
    """
    Xử lý hiển thị và cập nhật profile người dùng.
    - GET: Hiển thị biểu mẫu với thông tin hiện tại của người dùng.
    - POST: Cập nhật username và email với xác thực cơ bản.
    """
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Kiểm tra dữ liệu đầu vào
        if not username or not email:
            messages.error(request, 'Vui lòng nhập đầy đủ username và email.')
        elif len(username) < 3:
            messages.error(request, 'Username phải có ít nhất 3 ký tự.')
        else:
            try:
                # Kiểm tra username trùng lặp
                if username != user.username and User.objects.filter(username=username).exists():
                    messages.error(request, 'Username này đã được sử dụng.')
                else:
                    user.username = username
                    user.email = email
                    user.save()
                    messages.success(request, 'Hồ sơ của bạn đã được cập nhật thành công!')
                    return redirect('accounts:profile')
            except ValidationError as e:
                messages.error(request, f'Lỗi khi cập nhật: {str(e)}')
    return render(request, 'accounts/profile.html', {'user': request.user})