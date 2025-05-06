from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product
from accounts.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    session_id = models.CharField(_('Session ID'), max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name = _('Giỏ hàng')
        verbose_name_plural = _('Giỏ hàng')
    
    def __str__(self):
        return f"Giỏ hàng của {'khách' if self.user is None else self.user.email}"
    
    @property
    def total_quantity(self):
        """Return the total quantity of items in the cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        """Return the total price of all items in the cart"""
        return sum(item.total_price for item in self.items.all())
    
    def clear(self):
        """Remove all items from the cart"""
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('Số lượng'), default=1)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Chi tiết giỏ hàng')
        verbose_name_plural = _('Chi tiết giỏ hàng')
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total_price(self):
        """Return the total price for this item (quantity * price)"""
        return self.quantity * self.product.current_price
