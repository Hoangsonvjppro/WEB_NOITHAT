from django.contrib import admin
from .models import Branch, BranchImage


class BranchImageInline(admin.TabularInline):
    model = BranchImage
    extra = 1


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'is_active', 'staff_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'address')
    inlines = [BranchImageInline]
    readonly_fields = ('created_at', 'updated_at')
