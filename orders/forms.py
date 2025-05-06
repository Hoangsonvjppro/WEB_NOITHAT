from django import forms
from .models import Order


class CheckoutForm(forms.Form):
    shipping_name = forms.CharField(
        label='Họ và tên người nhận',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ và tên người nhận'})
    )
    shipping_email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập email'})
    )
    shipping_phone = forms.CharField(
        label='Số điện thoại',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'})
    )
    shipping_address = forms.CharField(
        label='Địa chỉ giao hàng',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Nhập địa chỉ giao hàng đầy đủ'})
    )
    payment_method = forms.ChoiceField(
        label='Phương thức thanh toán',
        choices=Order.PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    notes = forms.CharField(
        label='Ghi chú',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ghi chú về đơn hàng, ví dụ: thời gian hay chỉ dẫn địa điểm giao hàng chi tiết hơn.'})
    )


class PaymentForm(forms.Form):
    transaction_id = forms.CharField(
        label='Mã giao dịch',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        label='Ghi chú',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
