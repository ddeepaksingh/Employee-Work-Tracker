"""
Core app views: Activity Log list, Company Settings.
"""
import logging
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from apps.core.mixins import AdminRequiredMixin
from apps.core.models import ActivityLog, CompanySettings
from .forms import CompanySettingsForm

logger = logging.getLogger(__name__)


class ActivityLogListView(AdminRequiredMixin, ListView):
    model = ActivityLog
    template_name = 'core/activity_log_list.html'
    context_object_name = 'logs'
    paginate_by = 30

    def get_queryset(self):
        qs = ActivityLog.objects.select_related('user').order_by('-timestamp')
        action = self.request.GET.get('action', '')
        user_q = self.request.GET.get('user', '')
        if action:
            qs = qs.filter(action=action)
        if user_q:
            qs = qs.filter(user__username__icontains=user_q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_choices'] = ActivityLog.ACTION_CHOICES
        ctx['selected_action'] = self.request.GET.get('action', '')
        ctx['user_query'] = self.request.GET.get('user', '')
        return ctx


class CompanySettingsView(AdminRequiredMixin, UpdateView):
    model = CompanySettings
    form_class = CompanySettingsForm
    template_name = 'core/company_settings.html'
    success_url = reverse_lazy('core:settings')

    def get_object(self, queryset=None):
        return CompanySettings.get_settings()

    def form_valid(self, form):
        from apps.core.utils import log_activity, get_client_ip
        resp = super().form_valid(form)
        log_activity(self.request.user, 'SETTINGS_UPDATED', 'Company settings updated.', get_client_ip(self.request))
        messages.success(self.request, 'Company settings updated successfully.')
        return resp
