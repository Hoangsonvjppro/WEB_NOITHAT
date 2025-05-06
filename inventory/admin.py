from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from .models import Warehouse, InventoryRecord, StockMovement
from accounts.models import User


class InventoryRecordInline(admin.TabularInline):
    model = InventoryRecord
    extra = 0
    fields = ('product', 'quantity', 'location', 'min_stock_level', 'max_stock_level', 'is_low_stock')
    readonly_fields = ('is_low_stock',)


# Custom filter cho is_low_stock
class LowStockFilter(SimpleListFilter):
    title = 'Tình trạng tồn kho'
    parameter_name = 'stock_status'
    
    def lookups(self, request, model_admin):
        return (
            ('low', 'Sắp hết hàng'),
            ('normal', 'Bình thường'),
            ('over', 'Vượt mức'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(quantity__lt=models.F('min_stock_level'))
        if self.value() == 'normal':
            return queryset.filter(quantity__gte=models.F('min_stock_level'), quantity__lte=models.F('max_stock_level'))
        if self.value() == 'over':
            return queryset.filter(quantity__gt=models.F('max_stock_level'))


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'capacity', 'product_count', 'total_items', 'is_active')
    list_filter = ('is_active', 'branch')
    search_fields = ('name', 'address')
    inlines = [InventoryRecordInline]
    readonly_fields = ('created_at', 'updated_at', 'product_count', 'total_items')


@admin.register(InventoryRecord)
class InventoryRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'location', 'min_stock_level', 'max_stock_level', 'is_low_stock')
    list_filter = ('warehouse', LowStockFilter)
    search_fields = ('product__name', 'warehouse__name', 'location')
    readonly_fields = ('last_counted', 'is_low_stock', 'is_overstock')
    
    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Sắp hết hàng'


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'warehouse', 'destination_warehouse', 'product', 'quantity', 
                    'movement_type', 'performed_by', 'created_at')
    list_filter = ('movement_type', 'warehouse', 'created_at')
    search_fields = ('reference_number', 'product__name', 'warehouse__name')
    readonly_fields = ('reference_number', 'created_at')
    autocomplete_fields = ['product', 'warehouse', 'destination_warehouse', 'supplier', 'performed_by']
    date_hierarchy = 'created_at'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filter the users to only show inventory managers, branch managers and business owners
        if db_field.name == "performed_by":
            kwargs["queryset"] = User.objects.filter(
                role__in=['inventory_manager', 'branch_manager', 'business_owner']
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Set the current user as the default performer of the movement
        if not obj and hasattr(request, 'user') and request.user.is_authenticated:
            form.base_fields['performed_by'].initial = request.user
            
        return form
