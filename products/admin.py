from django.contrib import admin
from .models import Category, Product, ProductImage, ProductReview


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = False
    max_num = 0
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'quantity', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('price', 'discount_price', 'quantity', 'is_active', 'is_featured')
    inlines = [ProductImageInline, ProductReviewInline]
    fieldsets = (
        (None, {
            'fields': ('category', 'supplier', 'name', 'slug', 'sku', 'description')
        }),
        ('Giá & Số lượng', {
            'fields': ('price', 'cost_price', 'discount_price', 'quantity')
        }),
        ('Thông số kỹ thuật', {
            'fields': ('weight', 'dimensions', 'material', 'color')
        }),
        ('Trạng thái', {
            'fields': ('is_active', 'is_featured', 'created_at', 'updated_at')
        }),
    )


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__email', 'comment')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)
