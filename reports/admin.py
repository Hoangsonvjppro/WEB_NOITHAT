from django.contrib import admin
from .models import Report, ReportSchedule


class ReportScheduleInline(admin.TabularInline):
    model = ReportSchedule
    extra = 0
    fields = ('title', 'frequency', 'is_active', 'last_run', 'next_run')
    readonly_fields = ('last_run',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'branch', 'created_by', 'start_date', 'end_date', 'is_favorite', 'created_at')
    list_filter = ('report_type', 'branch', 'is_favorite', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    inlines = [ReportScheduleInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new report
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ReportSchedule)
class ReportScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'report', 'frequency', 'is_active', 'last_run', 'next_run')
    list_filter = ('frequency', 'is_active', 'last_run')
    search_fields = ('title', 'report__title')
    readonly_fields = ('last_run', 'created_at', 'updated_at')
    filter_horizontal = ('recipients',)
