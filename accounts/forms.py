from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomerProfile, StaffProfile

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    """Form đăng nhập tùy chỉnh"""
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu'}))

class CustomUserCreationForm(UserCreationForm):
    """Form đăng ký tùy chỉnh"""
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu'}))
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    """Form cập nhật thông tin người dùng"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomerProfileForm(forms.ModelForm):
    """Form cập nhật thông tin khách hàng"""
    class Meta:
        model = CustomerProfile
        fields = ('address', 'birth_date')
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
