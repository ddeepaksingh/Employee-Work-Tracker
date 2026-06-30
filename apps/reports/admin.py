"""
Reports app admin registration.
"""
from django.contrib import admin
from .models import DailyReport


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'word_count', 'is_edited', 'created_at')
    list_filter = ('date', 'is_edited', 'employee__department')
    search_fields = ('employee__user__username', 'report_text')
    readonly_fields = ('word_count', 'created_at', 'updated_at')
    date_hierarchy = 'date'
