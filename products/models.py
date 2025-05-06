from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from suppliers.models import Supplier


class Category(models.Model):
    name = models.CharField(_('Tên danh mục'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=120, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name=_('Danh mục cha'))
    description = models.TextField(_('Mô tả'), blank=True)
    image = models.ImageField(_('Hình ảnh'), upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(_('Kích hoạt'), default=True)
    order = models.PositiveIntegerField(_('Thứ tự'), default=0)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Danh mục')
        verbose_name_plural = _('Danh mục')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_('Danh mục'))
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products',
                                verbose_name=_('Nhà cung cấp'))
    name = models.CharField(_('Tên sản phẩm'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=220, unique=True)
    sku = models.CharField(_('Mã SKU'), max_length=50, unique=True, blank=True, null=True)
    description = models.TextField(_('Mô tả'), blank=True)
    price = models.DecimalField(_('Giá bán'), max_digits=12, decimal_places=2)
    cost_price = models.DecimalField(_('Giá nhập'), max_digits=12, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(_('Giá khuyến mãi'), max_digits=12, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(_('Số lượng'), default=0)
    weight = models.DecimalField(_('Trọng lượng (kg)'), max_digits=8, decimal_places=2, null=True, blank=True)
    dimensions = models.CharField(_('Kích thước (DxRxC cm)'), max_length=100, blank=True)
    material = models.CharField(_('Chất liệu'), max_length=100, blank=True)
    color = models.CharField(_('Màu sắc'), max_length=50, blank=True)
    is_featured = models.BooleanField(_('Nổi bật'), default=False)
    is_active = models.BooleanField(_('Hiển thị'), default=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Sản phẩm')
        verbose_name_plural = _('Sản phẩm')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = f"P{self.id:07d}" if self.id else None
        super().save(*args, **kwargs)
        if not self.sku:
            self.sku = f"P{self.id:07d}"
            self.save(update_fields=['sku'])
    
    @property
    def current_price(self):
        """Return the discount price if it exists, otherwise return the regular price"""
        return self.discount_price if self.discount_price else self.price
    
    @property
    def discount_percentage(self):
        """Return the discount percentage if discount price exists"""
        if self.discount_price and self.price > 0:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    @property
    def is_in_stock(self):
        """Return True if the product is in stock, False otherwise"""
        return self.quantity > 0
    
    @property
    def average_rating(self):
        """Return the average rating of the product"""
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('Sản phẩm'))
    image = models.ImageField(_('Hình ảnh'), upload_to='products/')
    is_primary = models.BooleanField(_('Ảnh chính'), default=False)
    alt_text = models.CharField(_('Mô tả ảnh'), max_length=255, blank=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Hình ảnh sản phẩm')
        verbose_name_plural = _('Hình ảnh sản phẩm')
        ordering = ['-is_primary', 'created_at']
    
    def __str__(self):
        return f"Hình ảnh của {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other images of this product as not primary
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Sản phẩm'))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Người dùng'))
    rating = models.PositiveSmallIntegerField(_('Đánh giá'), choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(_('Bình luận'), blank=True)
    created_at = models.DateTimeField(_('Ngày tạo'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Cập nhật lần cuối'), auto_now=True)
    
    class Meta:
        verbose_name = _('Đánh giá sản phẩm')
        verbose_name_plural = _('Đánh giá sản phẩm')
        ordering = ['-created_at']
        unique_together = ('product', 'user')
    
    def __str__(self):
        return f"{self.user.get_full_name()} đánh giá {self.product.name}"
