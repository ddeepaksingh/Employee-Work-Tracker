"""
Reusable mixins for role-based access control.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect


class AdminRequiredMixin(LoginRequiredMixin):
    """Restricts access to admin (staff) users only."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard:index')
        return super().dispatch(request, *args, **kwargs)


class EmployeeRequiredMixin(LoginRequiredMixin):
    """Ensures user is authenticated. Employees only (non-staff)."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnershipMixin:
    """Ensures the requesting employee owns the object."""

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if hasattr(obj, 'employee'):
            profile = getattr(self.request.user, 'employee_profile', None)
            if not self.request.user.is_staff and obj.employee != profile:
                raise PermissionDenied
        return obj
