from django.db import models
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    name = models.CharField(_('Tên chi nhánh'), max_length=100)
    address = models.TextField(_('Địa chỉ'))
    phone = models.CharField(_('Số điện thoại'), max_length=15)
    email = models.EmailField(_('Email liên hệ'), blank=True)
    opening_hours = models.CharField(_('Giờ mở cửa'), max_length=100, default='08:00 - 22:00')
    is_active = models.BooleanField(_('Đang hoạt động'), default=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Chi nhánh')
        verbose_name_plural = _('Chi nhánh')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def manager(self):
        """Return the manager of this branch"""
        manager = self.staff.filter(user__role='branch_manager').first()
        return manager
    
    @property
    def staff_count(self):
        """Return the number of staff in this branch"""
        return self.staff.count()


class BranchImage(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('Hình ảnh'), upload_to='branches/')
    description = models.CharField(_('Mô tả'), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _('Hình ảnh chi nhánh')
        verbose_name_plural = _('Hình ảnh chi nhánh')
    
    def __str__(self):
        return f"Hình ảnh của {self.branch.name}"
