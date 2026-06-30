"""
Dashboard app views: Employee and Admin dashboards with analytics.
"""
import json
import logging
from datetime import date, timedelta
from calendar import month_name

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, View

from apps.core.mixins import AdminRequiredMixin, EmployeeRequiredMixin
from apps.employees.models import Department, EmployeeProfile
from apps.reports.models import DailyReport
from apps.notifications.models import Notification

logger = logging.getLogger(__name__)
User = get_user_model()


class IndexRedirectView(View):
    """Redirect root URL to the appropriate dashboard."""

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return redirect('dashboard:index')


class DashboardView(EmployeeRequiredMixin, View):
    """Routes to admin or employee dashboard based on role."""

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return AdminDashboardView.as_view()(request, *args, **kwargs)
        return EmployeeDashboardView.as_view()(request, *args, **kwargs)


class EmployeeDashboardView(EmployeeRequiredMixin, TemplateView):
    """Employee's personal dashboard."""

    template_name = 'dashboard/employee_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        today = date.today()

        try:
            profile = user.employee_profile
        except EmployeeProfile.DoesNotExist:
            profile = None

        ctx['profile'] = profile
        ctx['today'] = today

        if profile:
            ctx['today_report'] = DailyReport.objects.filter(employee=profile, date=today).first()
            ctx['report_submitted_today'] = ctx['today_report'] is not None
            ctx['recent_reports'] = DailyReport.objects.filter(employee=profile).order_by('-date')[:7]
            ctx['total_reports'] = DailyReport.objects.filter(employee=profile).count()
            ctx['this_month_reports'] = DailyReport.objects.filter(
                employee=profile, date__year=today.year, date__month=today.month
            ).count()
            ctx['this_week_reports'] = DailyReport.objects.filter(
                employee=profile, date__gte=today - timedelta(days=7)
            ).count()
        return ctx


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """Admin dashboard with KPI cards and analytics charts."""

    template_name = 'dashboard/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()

        # ── KPI Cards ────────────────────────────────────────────────────────
        ctx['total_employees'] = EmployeeProfile.objects.filter(is_active=True).count()
        ctx['total_departments'] = Department.objects.filter(is_active=True).count()
        ctx['total_reports'] = DailyReport.objects.count()

        submitted_today_ids = DailyReport.objects.filter(date=today).values_list('employee_id', flat=True)
        ctx['submitted_today'] = len(submitted_today_ids)
        ctx['pending_today'] = EmployeeProfile.objects.filter(is_active=True).exclude(id__in=submitted_today_ids).count()

        this_month_count = DailyReport.objects.filter(
            date__year=today.year, date__month=today.month
        ).count()
        ctx['this_month_reports'] = this_month_count

        # ── Recent Activity ──────────────────────────────────────────────────
        ctx['latest_reports'] = DailyReport.objects.select_related('employee__user').order_by('-created_at')[:8]
        ctx['recent_employees'] = EmployeeProfile.objects.select_related('user', 'department').order_by('-created_at')[:5]
        ctx['pending_employees'] = EmployeeProfile.objects.filter(
            is_active=True
        ).exclude(id__in=submitted_today_ids).select_related('user', 'department')[:10]

        # ── Chart: Daily submissions last 14 days ───────────────────────────
        daily_data = (
            DailyReport.objects
            .filter(date__gte=today - timedelta(days=13))
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        daily_labels = [(today - timedelta(days=13 - i)).strftime('%d %b') for i in range(14)]
        daily_counts_map = {entry['day'].strftime('%d %b'): entry['count'] for entry in daily_data}
        daily_counts = [daily_counts_map.get(label, 0) for label in daily_labels]
        ctx['daily_chart_labels'] = json.dumps(daily_labels)
        ctx['daily_chart_data'] = json.dumps(daily_counts)

        # ── Chart: Monthly submissions last 6 months ─────────────────────────
        monthly_data = (
            DailyReport.objects
            .filter(date__gte=today - timedelta(days=180))
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        monthly_labels = [entry['month'].strftime('%b %Y') for entry in monthly_data]
        monthly_counts = [entry['count'] for entry in monthly_data]
        ctx['monthly_chart_labels'] = json.dumps(monthly_labels)
        ctx['monthly_chart_data'] = json.dumps(monthly_counts)

        # ── Chart: Department-wise reports ───────────────────────────────────
        dept_data = (
            DailyReport.objects
            .values('employee__department__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:8]
        )
        ctx['dept_chart_labels'] = json.dumps([d['employee__department__name'] or 'Unassigned' for d in dept_data])
        ctx['dept_chart_data'] = json.dumps([d['count'] for d in dept_data])

        # ── Top/Bottom employees ──────────────────────────────────────────────
        ctx['top_employees'] = (
            EmployeeProfile.objects
            .annotate(report_count=Count('daily_reports'))
            .filter(is_active=True)
            .order_by('-report_count')[:5]
        )

        return ctx
