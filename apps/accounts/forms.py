from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tùy chỉnh help_text để thay đổi thông báo
        self.fields['username'].help_text = 'Bắt buộc. Tối đa 150 ký tự. Chỉ chấp nhận chữ cái, số và @/./+/-/_.'
        self.fields['password1'].help_text = 'Mật khẩu phải có ít nhất 6 ký tự.'
        self.fields['password2'].help_text = 'Nhập lại mật khẩu để xác nhận.'

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Nới lỏng yêu cầu: Chỉ yêu cầu ít nhất 6 ký tự
        if len(password1) < 6:
            raise ValidationError("Mật khẩu phải có ít nhất 6 ký tự.")
        return password1