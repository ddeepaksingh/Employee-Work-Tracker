"""
Reports app admin registration.
"""
from django.contrib import admin
from .models import DailyReport, Activity, DailyReportActivity


class DailyReportActivityInline(admin.TabularInline):
    model = DailyReportActivity
    extra = 0
    autocomplete_fields = ('activity',)


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('get_employee_id', 'get_employee_name', 'date', 'word_count', 'is_edited', 'created_at')
    list_filter = ('date', 'is_edited', 'employee__department')
    search_fields = ('employee__user__username', 'employee__employee_id', 'employee__user__first_name', 'employee__user__last_name', 'report_text')
    readonly_fields = ('word_count', 'created_at', 'updated_at')
    date_hierarchy = 'date'
    inlines = [DailyReportActivityInline]

    def get_employee_id(self, obj):
        return obj.employee.employee_id
    get_employee_id.short_description = 'Employee ID'
    get_employee_id.admin_order_field = 'employee__employee_id'

    def get_employee_name(self, obj):
        return obj.employee.full_name
    get_employee_name.short_description = 'Employee Name'
    get_employee_name.admin_order_field = 'employee__user__first_name'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

