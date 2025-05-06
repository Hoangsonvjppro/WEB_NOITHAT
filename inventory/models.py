from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product
from branches.models import Branch
from suppliers.models import Supplier
from accounts.models import User


class Warehouse(models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='warehouse')
    name = models.CharField(_('Tên kho'), max_length=100)
    capacity = models.PositiveIntegerField(_('Sức chứa (m²)'), default=0)
    address = models.TextField(_('Địa chỉ'), blank=True)
    description = models.TextField(_('Mô tả'), blank=True)
    is_active = models.BooleanField(_('Đang hoạt động'), default=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Kho')
        verbose_name_plural = _('Kho')
    
    def __str__(self):
        return self.name
    
    @property
    def product_count(self):
        """Return the number of distinct products in the warehouse"""
        return self.inventory_records.count()
    
    @property
    def total_items(self):
        """Return the total quantity of all products in the warehouse"""
        return sum(record.quantity for record in self.inventory_records.all())


class InventoryRecord(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory_records')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_records')
    quantity = models.PositiveIntegerField(_('Số lượng'), default=0)
    location = models.CharField(_('Vị trí'), max_length=50, blank=True, help_text=_('Ví dụ: A12, B5, ...'))
    min_stock_level = models.PositiveIntegerField(_('Mức tồn kho tối thiểu'), default=5)
    max_stock_level = models.PositiveIntegerField(_('Mức tồn kho tối đa'), default=100)
    last_counted = models.DateTimeField(_('Kiểm kê lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Tồn kho')
        verbose_name_plural = _('Tồn kho')
        unique_together = ('warehouse', 'product')
    
    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}"
    
    @property
    def is_low_stock(self):
        """Check if the stock level is below the minimum threshold"""
        return self.quantity < self.min_stock_level
    
    @property
    def is_overstock(self):
        """Check if the stock level is above the maximum threshold"""
        return self.quantity > self.max_stock_level


class StockMovement(models.Model):
    MOVEMENT_IN = 'in'
    MOVEMENT_OUT = 'out'
    MOVEMENT_TRANSFER = 'transfer'
    MOVEMENT_ADJUSTMENT = 'adjustment'
    MOVEMENT_RETURN = 'return'
    
    MOVEMENT_TYPE_CHOICES = [
        (MOVEMENT_IN, _('Nhập kho')),
        (MOVEMENT_OUT, _('Xuất kho')),
        (MOVEMENT_TRANSFER, _('Chuyển kho')),
        (MOVEMENT_ADJUSTMENT, _('Điều chỉnh')),
        (MOVEMENT_RETURN, _('Trả hàng')),
    ]
    
    reference_number = models.CharField(_('Mã tham chiếu'), max_length=50, unique=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_movements')
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, 
                                            related_name='incoming_movements')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    quantity = models.PositiveIntegerField(_('Số lượng'))
    movement_type = models.CharField(_('Loại'), max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.DecimalField(_('Đơn giá'), max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(_('Ghi chú'), blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_movements')
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Lịch sử xuất nhập kho')
        verbose_name_plural = _('Lịch sử xuất nhập kho')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} - {self.quantity} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            prefix = {
                self.MOVEMENT_IN: 'IN',
                self.MOVEMENT_OUT: 'OUT',
                self.MOVEMENT_TRANSFER: 'TR',
                self.MOVEMENT_ADJUSTMENT: 'ADJ',
                self.MOVEMENT_RETURN: 'RET',
            }.get(self.movement_type, 'MOV')
            
            # Generate a sequential number
            last_movement = StockMovement.objects.order_by('-id').first()
            last_id = last_movement.id if last_movement else 0
            self.reference_number = f"{prefix}{last_id + 1:08d}"
        
        # Update inventory record quantities
        inventory_record, created = InventoryRecord.objects.get_or_create(
            warehouse=self.warehouse,
            product=self.product,
            defaults={'quantity': 0}
        )
        
        # Handle different movement types
        if self.movement_type == self.MOVEMENT_IN or self.movement_type == self.MOVEMENT_RETURN:
            inventory_record.quantity += self.quantity
        elif self.movement_type == self.MOVEMENT_OUT:
            inventory_record.quantity = max(0, inventory_record.quantity - self.quantity)
        elif self.movement_type == self.MOVEMENT_TRANSFER and self.destination_warehouse:
            inventory_record.quantity = max(0, inventory_record.quantity - self.quantity)
            dest_record, dest_created = InventoryRecord.objects.get_or_create(
                warehouse=self.destination_warehouse,
                product=self.product,
                defaults={'quantity': 0}
            )
            dest_record.quantity += self.quantity
            dest_record.save()
        
        inventory_record.save()
        
        super().save(*args, **kwargs)
