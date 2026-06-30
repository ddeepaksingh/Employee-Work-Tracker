"""
Employees app admin registration.
"""
from django.contrib import admin
from .models import Department, Designation, EmployeeProfile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_count', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'is_active', 'created_at')
    list_filter = ('department', 'is_active')
    search_fields = ('name',)


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'department', 'designation', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')
    raw_id_fields = ('user',)
