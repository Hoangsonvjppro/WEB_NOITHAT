from django.contrib import admin
from .models import Supplier, SupplyDetail


class SupplyDetailInline(admin.TabularInline):
    model = SupplyDetail
    extra = 1
    fields = ('supply_date', 'reference_number', 'total_amount', 'payment_status')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'phone', 'email', 'is_active', 'product_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'contact_name', 'phone', 'email')
    inlines = [SupplyDetailInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SupplyDetail)
class SupplyDetailAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'supply_date', 'reference_number', 'total_amount', 'payment_status')
    list_filter = ('payment_status', 'supply_date')
    search_fields = ('supplier__name', 'reference_number')
    date_hierarchy = 'supply_date'
    readonly_fields = ('created_at', 'updated_at')
