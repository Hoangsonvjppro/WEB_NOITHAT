from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'total_price')
    fields = ('product', 'product_name', 'price', 'quantity', 'total_price')
    can_delete = False


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('amount', 'payment_method', 'transaction_id', 'is_successful', 'notes', 'created_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'shipping_name', 'status', 'payment_status', 
                    'total_amount', 'created_at', 'branch')
    list_filter = ('status', 'payment_status', 'branch', 'created_at')
    search_fields = ('order_number', 'user__email', 'shipping_name', 'shipping_phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'subtotal', 'total_items')
    inlines = [OrderItemInline, PaymentInline]
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('order_number', 'user', 'branch', 'status', 'created_at', 'updated_at')
        }),
        ('Thông tin giao hàng', {
            'fields': ('shipping_name', 'shipping_phone', 'shipping_email', 'shipping_address', 'tracking_number')
        }),
        ('Thông tin thanh toán', {
            'fields': ('payment_method', 'payment_status', 'subtotal', 'shipping_fee', 'discount_amount', 'tax_amount', 'total_amount')
        }),
        ('Ghi chú', {
            'fields': ('notes',)
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Only allow staff with branch_manager or business_owner role to change order status
        if not request.user.is_superuser and obj and not (
            hasattr(request.user, 'role') and 
            request.user.role in ['branch_manager', 'business_owner', 'sales_staff']
        ):
            form.base_fields['status'].disabled = True
            form.base_fields['payment_status'].disabled = True
        return form


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'is_successful', 'created_at')
    list_filter = ('payment_method', 'is_successful', 'created_at')
    search_fields = ('order__order_number', 'transaction_id')
    readonly_fields = ('created_at',)
