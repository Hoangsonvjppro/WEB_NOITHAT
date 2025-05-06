from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'total_price')
    readonly_fields = ('total_price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'total_quantity', 'total_price', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at', 'total_quantity', 'total_price')
    inlines = [CartItemInline]
    actions = ['clear_carts']
    
    def clear_carts(self, request, queryset):
        for cart in queryset:
            cart.clear()
        self.message_user(request, f"{queryset.count()} giỏ hàng đã được xóa hết sản phẩm.")
    clear_carts.short_description = "Xóa hết sản phẩm khỏi giỏ hàng đã chọn"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price', 'updated_at')
    list_filter = ('cart__user',)
    search_fields = ('cart__user__email', 'product__name')
    readonly_fields = ('total_price',)
