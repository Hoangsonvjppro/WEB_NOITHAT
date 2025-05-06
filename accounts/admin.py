from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, CustomerProfile, StaffProfile


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Thông tin khách hàng'


class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    can_delete = False
    verbose_name_plural = 'Thông tin nhân viên'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Thông tin cá nhân'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Quyền hạn'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Ngày tham gia'), {'fields': ('date_joined', 'last_login')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    
    def get_inlines(self, request, obj=None):
        if obj:
            if obj.is_customer:
                return [CustomerProfileInline]
            elif obj.is_sales_staff or obj.is_inventory_manager or obj.is_branch_manager or obj.is_business_owner:
                return [StaffProfileInline]
        return []
