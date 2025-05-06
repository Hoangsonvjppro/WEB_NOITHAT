from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from branches.models import Branch


class Report(models.Model):
    REPORT_TYPE_SALES = 'sales'
    REPORT_TYPE_INVENTORY = 'inventory'
    REPORT_TYPE_PERFORMANCE = 'performance'
    REPORT_TYPE_FINANCIAL = 'financial'
    
    REPORT_TYPE_CHOICES = [
        (REPORT_TYPE_SALES, _('Báo cáo bán hàng')),
        (REPORT_TYPE_INVENTORY, _('Báo cáo tồn kho')),
        (REPORT_TYPE_PERFORMANCE, _('Báo cáo hiệu suất')),
        (REPORT_TYPE_FINANCIAL, _('Báo cáo tài chính')),
    ]
    
    title = models.CharField(_('Tiêu đề'), max_length=255)
    report_type = models.CharField(_('Loại báo cáo'), max_length=20, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(_('Mô tả'), blank=True)
    parameters = models.JSONField(_('Tham số'), default=dict, blank=True, 
                                help_text=_('Các tham số được sử dụng để tạo báo cáo, dạng JSON'))
    result_data = models.JSONField(_('Dữ liệu kết quả'), default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    start_date = models.DateField(_('Ngày bắt đầu'), null=True, blank=True)
    end_date = models.DateField(_('Ngày kết thúc'), null=True, blank=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    is_favorite = models.BooleanField(_('Yêu thích'), default=False)
    
    class Meta:
        verbose_name = _('Báo cáo')
        verbose_name_plural = _('Báo cáo')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class ReportSchedule(models.Model):
    FREQUENCY_DAILY = 'daily'
    FREQUENCY_WEEKLY = 'weekly'
    FREQUENCY_MONTHLY = 'monthly'
    FREQUENCY_QUARTERLY = 'quarterly'
    
    FREQUENCY_CHOICES = [
        (FREQUENCY_DAILY, _('Hàng ngày')),
        (FREQUENCY_WEEKLY, _('Hàng tuần')),
        (FREQUENCY_MONTHLY, _('Hàng tháng')),
        (FREQUENCY_QUARTERLY, _('Hàng quý')),
    ]
    
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='schedules')
    title = models.CharField(_('Tiêu đề'), max_length=255)
    frequency = models.CharField(_('Tần suất'), max_length=20, choices=FREQUENCY_CHOICES)
    recipients = models.ManyToManyField(User, related_name='report_subscriptions')
    is_active = models.BooleanField(_('Kích hoạt'), default=True)
    last_run = models.DateTimeField(_('Lần chạy cuối'), null=True, blank=True)
    next_run = models.DateTimeField(_('Lần chạy kế tiếp'), null=True, blank=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Lịch báo cáo')
        verbose_name_plural = _('Lịch báo cáo')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
