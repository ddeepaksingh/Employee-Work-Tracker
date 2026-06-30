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
    report_text = models.TextField()
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
        self.word_count = len(self.report_text.split())
        super().save(*args, **kwargs)

    @property
    def char_count(self) -> int:
        return len(self.report_text)
