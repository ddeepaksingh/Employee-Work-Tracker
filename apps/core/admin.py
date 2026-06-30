"""
Core app admin registration.
"""
from django.contrib import admin
from .models import ActivityLog, CompanySettings


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'timestamp')
    list_filter = ('action',)
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('user', 'action', 'description', 'ip_address', 'timestamp', 'extra_data')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'timezone', 'theme', 'updated_at')

    def has_add_permission(self, request):
        return not CompanySettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
