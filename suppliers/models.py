from django.db import models
from django.utils.translation import gettext_lazy as _


class Supplier(models.Model):
    name = models.CharField(_('Tên nhà cung cấp'), max_length=100)
    contact_name = models.CharField(_('Tên người liên hệ'), max_length=100, blank=True)
    address = models.TextField(_('Địa chỉ'), blank=True)
    phone = models.CharField(_('Số điện thoại'), max_length=15)
    email = models.EmailField(_('Email'), blank=True)
    description = models.TextField(_('Mô tả'), blank=True)
    is_active = models.BooleanField(_('Đang hoạt động'), default=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Nhà cung cấp')
        verbose_name_plural = _('Nhà cung cấp')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def product_count(self):
        """Return the number of products supplied by this supplier"""
        return self.products.count()
    
    @property
    def last_supply_date(self):
        """Return the date of the last supply from this supplier"""
        last_supply = self.supply_details.order_by('-supply_date').first()
        return last_supply.supply_date if last_supply else None


class SupplyDetail(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supply_details')
    supply_date = models.DateField(_('Ngày cung cấp'))
    reference_number = models.CharField(_('Số tham chiếu'), max_length=50, blank=True)
    total_amount = models.DecimalField(_('Tổng tiền'), max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(_('Trạng thái thanh toán'), max_length=20, 
                                    choices=[
                                        ('pending', _('Chưa thanh toán')),
                                        ('partial', _('Thanh toán một phần')),
                                        ('paid', _('Đã thanh toán'))
                                    ], default='pending')
    notes = models.TextField(_('Ghi chú'), blank=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Chi tiết cung cấp')
        verbose_name_plural = _('Chi tiết cung cấp')
        ordering = ['-supply_date']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.supply_date} - {self.reference_number}"
