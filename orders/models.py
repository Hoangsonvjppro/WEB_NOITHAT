from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from products.models import Product
from branches.models import Branch


class Order(models.Model):
    # Order status choices
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    STATUS_RETURNED = 'returned'
    STATUS_REFUNDED = 'refunded'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Chờ xác nhận')),
        (STATUS_PROCESSING, _('Đang xử lý')),
        (STATUS_SHIPPED, _('Đang giao hàng')),
        (STATUS_DELIVERED, _('Đã giao hàng')),
        (STATUS_CANCELLED, _('Đã hủy')),
        (STATUS_RETURNED, _('Đã trả hàng')),
        (STATUS_REFUNDED, _('Đã hoàn tiền')),
    ]
    
    # Payment status choices
    PAYMENT_PENDING = 'pending'
    PAYMENT_PAID = 'paid'
    PAYMENT_FAILED = 'failed'
    PAYMENT_REFUNDED = 'refunded'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, _('Chưa thanh toán')),
        (PAYMENT_PAID, _('Đã thanh toán')),
        (PAYMENT_FAILED, _('Thanh toán thất bại')),
        (PAYMENT_REFUNDED, _('Đã hoàn tiền')),
    ]
    
    # Payment method choices
    PAYMENT_METHOD_COD = 'cod'
    PAYMENT_METHOD_BANK_TRANSFER = 'bank_transfer'
    PAYMENT_METHOD_CREDIT_CARD = 'credit_card'
    PAYMENT_METHOD_MOMO = 'momo'
    PAYMENT_METHOD_ZALOPAY = 'zalopay'
    
    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_COD, _('Thanh toán khi nhận hàng')),
        (PAYMENT_METHOD_BANK_TRANSFER, _('Chuyển khoản ngân hàng')),
        (PAYMENT_METHOD_CREDIT_CARD, _('Thẻ tín dụng/ghi nợ')),
        (PAYMENT_METHOD_MOMO, _('Ví MoMo')),
        (PAYMENT_METHOD_ZALOPAY, _('ZaloPay')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    order_number = models.CharField(_('Mã đơn hàng'), max_length=20, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = models.CharField(_('Trạng thái'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    shipping_address = models.TextField(_('Địa chỉ giao hàng'))
    shipping_phone = models.CharField(_('Số điện thoại giao hàng'), max_length=15)
    shipping_name = models.CharField(_('Tên người nhận'), max_length=100)
    shipping_email = models.EmailField(_('Email'), blank=True)
    shipping_fee = models.DecimalField(_('Phí vận chuyển'), max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('Giảm giá'), max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_('Thuế'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('Tổng tiền'), max_digits=12, decimal_places=2)
    notes = models.TextField(_('Ghi chú'), blank=True)
    payment_method = models.CharField(_('Phương thức thanh toán'), max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(_('Trạng thái thanh toán'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    tracking_number = models.CharField(_('Mã vận đơn'), max_length=50, blank=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    delivered_at = models.DateTimeField(_('Ngày giao hàng'), null=True, blank=True)
    cancelled_at = models.DateTimeField(_('Ngày hủy'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Đơn hàng')
        verbose_name_plural = _('Đơn hàng')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Đơn hàng #{self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number and self.id:
            self.order_number = f"ORD{self.id:07d}"
        super().save(*args, **kwargs)
    
    @property
    def subtotal(self):
        """Return the subtotal (before shipping, tax, and discount)"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_items(self):
        """Return the total number of items in the order"""
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(_('Tên sản phẩm'), max_length=200)  # Store name in case product is deleted
    quantity = models.PositiveIntegerField(_('Số lượng'))
    price = models.DecimalField(_('Đơn giá'), max_digits=12, decimal_places=2)  # Price at time of order
    total_price = models.DecimalField(_('Thành tiền'), max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = _('Chi tiết đơn hàng')
        verbose_name_plural = _('Chi tiết đơn hàng')
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(_('Số tiền'), max_digits=12, decimal_places=2)
    payment_method = models.CharField(_('Phương thức thanh toán'), max_length=20, choices=Order.PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(_('Mã giao dịch'), max_length=100, blank=True)
    is_successful = models.BooleanField(_('Thành công'), default=False)
    notes = models.TextField(_('Ghi chú'), blank=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Thanh toán')
        verbose_name_plural = _('Thanh toán')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_payment_method_display()} - {self.amount} - {self.created_at.strftime('%d/%m/%Y')}"
