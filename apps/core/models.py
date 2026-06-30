"""
Core app models: ActivityLog and CompanySettings.
"""
import logging
from django.db import models
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


class ActivityLog(models.Model):
    """Records every significant action performed in the system."""

    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('REPORT_CREATED', 'Report Created'),
        ('REPORT_UPDATED', 'Report Updated'),
        ('REPORT_DELETED', 'Report Deleted'),
        ('EMPLOYEE_ADDED', 'Employee Added'),
        ('EMPLOYEE_EDITED', 'Employee Edited'),
        ('EMPLOYEE_DELETED', 'Employee Deleted'),
        ('PASSWORD_CHANGED', 'Password Changed'),
        ('PASSWORD_RESET', 'Password Reset'),
        ('DEPARTMENT_CREATED', 'Department Created'),
        ('DEPARTMENT_UPDATED', 'Department Updated'),
        ('DESIGNATION_CREATED', 'Designation Created'),
        ('DESIGNATION_UPDATED', 'Designation Updated'),
        ('SETTINGS_UPDATED', 'Settings Updated'),
        ('EXPORT', 'Data Exported'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs',
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self) -> str:
        username = self.user.username if self.user else 'Anonymous'
        return f"{username} — {self.get_action_display()} at {self.timestamp:%Y-%m-%d %H:%M}"


class CompanySettings(models.Model):
    """Singleton model for company-wide application settings."""

    company_name = models.CharField(max_length=200, default='My Company')
    company_logo = models.ImageField(upload_to='company/', null=True, blank=True)
    timezone = models.CharField(max_length=100, default='Asia/Kolkata')
    date_format = models.CharField(
        max_length=30,
        default='%d %B %Y',
        help_text='Python strftime format string',
    )
    submission_deadline = models.TimeField(
        default='23:59',
        help_text='Daily report submission deadline (HH:MM)',
    )
    footer_text = models.CharField(
        max_length=300,
        default='© 2025 My Company. All rights reserved.',
    )
    theme = models.CharField(
        max_length=10,
        choices=[('light', 'Light'), ('dark', 'Dark')],
        default='light',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company Settings'
        verbose_name_plural = 'Company Settings'

    def __str__(self) -> str:
        return self.company_name

    @classmethod
    def get_settings(cls) -> 'CompanySettings':
        """Return the singleton settings object, creating it if needed."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
