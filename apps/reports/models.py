"""
Reports app models: DailyReport.
"""
import logging
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)


class DailyReport(models.Model):
    """An employee's daily work report — one per employee per day."""

    employee = models.ForeignKey(
        'employees.EmployeeProfile',
        on_delete=models.CASCADE,
        related_name='daily_reports',
    )
    date = models.DateField(default=timezone.localdate)
    report_text = models.TextField(blank=True)
    word_count = models.PositiveIntegerField(default=0, editable=False)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        unique_together = [('employee', 'date')]
        verbose_name = 'Daily Report'
        verbose_name_plural = 'Daily Reports'

    def __str__(self) -> str:
        return f"{self.employee.full_name} — {self.date}"

    def get_absolute_url(self) -> str:
        return reverse('reports:report_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs) -> None:
        if self.pk:
            activities_list = self.activities.select_related('activity').all()
            if activities_list.exists():
                compiled_parts = []
                for ra in activities_list:
                    compiled_parts.append(
                        f"Activity: {ra.activity.name}\nQuantity: {ra.quantity}\nReport: {ra.report_text}"
                    )
                self.report_text = "\n\n---\n\n".join(compiled_parts)

        self.word_count = len(self.report_text.split()) if self.report_text else 0
        super().save(*args, **kwargs)

    @property
    def char_count(self) -> int:
        return len(self.report_text) if self.report_text else 0


class Activity(models.Model):
    """Admin-defined work activities."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class DailyReportActivity(models.Model):
    """Individual activity entry submitted under a DailyReport."""

    daily_report = models.ForeignKey(
        DailyReport,
        on_delete=models.CASCADE,
        related_name='activities',
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='report_entries',
    )
    report_text = models.TextField()
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Daily Report Activity'
        verbose_name_plural = 'Daily Report Activities'

    def __str__(self) -> str:
        return f"{self.activity.name} ({self.quantity}) — {self.daily_report.employee.full_name}"

