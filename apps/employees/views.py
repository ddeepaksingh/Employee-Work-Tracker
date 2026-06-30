"""
Employee app views: Department CRUD, Designation CRUD, Employee CRUD.
"""
import logging
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from apps.core.mixins import AdminRequiredMixin, EmployeeRequiredMixin
from apps.core.utils import log_activity, get_client_ip, send_notification
from .models import Department, Designation, EmployeeProfile
from .forms import (
    DepartmentForm, DesignationForm,
    EmployeeCreateForm, EmployeeEditForm, EmployeeProfileSelfEditForm,
    AdminResetPasswordForm,
)

logger = logging.getLogger(__name__)
User = get_user_model()


# ── Department Views ─────────────────────────────────────────────────────────

class DepartmentListView(AdminRequiredMixin, ListView):
    model = Department
    template_name = 'employees/department_list.html'
    context_object_name = 'departments'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx


class DepartmentCreateView(AdminRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('employees:department_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        log_activity(self.request.user, 'DEPARTMENT_CREATED', f"Department '{self.object.name}' created.", get_client_ip(self.request))
        messages.success(self.request, f"Department '{self.object.name}' created successfully.")
        return resp


class DepartmentUpdateView(AdminRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('employees:department_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        log_activity(self.request.user, 'DEPARTMENT_UPDATED', f"Department '{self.object.name}' updated.", get_client_ip(self.request))
        messages.success(self.request, f"Department '{self.object.name}' updated.")
        return resp


class DepartmentDeleteView(AdminRequiredMixin, DeleteView):
    model = Department
    template_name = 'employees/department_confirm_delete.html'
    success_url = reverse_lazy('employees:department_list')

    def form_valid(self, form):
        name = self.object.name
        resp = super().form_valid(form)
        messages.success(self.request, f"Department '{name}' deleted.")
        return resp


# ── Designation Views ────────────────────────────────────────────────────────

class DesignationListView(AdminRequiredMixin, ListView):
    model = Designation
    template_name = 'employees/designation_list.html'
    context_object_name = 'designations'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('department')
        dept = self.request.GET.get('department', '')
        q = self.request.GET.get('q', '')
        if dept:
            qs = qs.filter(department_id=dept)
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['departments'] = Department.objects.filter(is_active=True)
        ctx['selected_dept'] = self.request.GET.get('department', '')
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx


class DesignationCreateView(AdminRequiredMixin, CreateView):
    model = Designation
    form_class = DesignationForm
    template_name = 'employees/designation_form.html'
    success_url = reverse_lazy('employees:designation_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        log_activity(self.request.user, 'DESIGNATION_CREATED', f"Designation '{self.object.name}' created.", get_client_ip(self.request))
        messages.success(self.request, f"Designation '{self.object.name}' created successfully.")
        return resp


class DesignationUpdateView(AdminRequiredMixin, UpdateView):
    model = Designation
    form_class = DesignationForm
    template_name = 'employees/designation_form.html'
    success_url = reverse_lazy('employees:designation_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        log_activity(self.request.user, 'DESIGNATION_UPDATED', f"Designation '{self.object.name}' updated.", get_client_ip(self.request))
        messages.success(self.request, f"Designation '{self.object.name}' updated.")
        return resp


class DesignationDeleteView(AdminRequiredMixin, DeleteView):
    model = Designation
    template_name = 'employees/designation_confirm_delete.html'
    success_url = reverse_lazy('employees:designation_list')

    def form_valid(self, form):
        name = self.object.name
        resp = super().form_valid(form)
        messages.success(self.request, f"Designation '{name}' deleted.")
        return resp


# ── Employee Views ───────────────────────────────────────────────────────────

class EmployeeListView(AdminRequiredMixin, ListView):
    model = EmployeeProfile
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20

    def get_queryset(self):
        qs = EmployeeProfile.objects.select_related('user', 'department', 'designation')
        q = self.request.GET.get('q', '')
        dept = self.request.GET.get('department', '')
        status = self.request.GET.get('status', '')
        if q:
            qs = qs.filter(
                user__first_name__icontains=q
            ) | qs.filter(user__last_name__icontains=q) | qs.filter(employee_id__icontains=q)
        if dept:
            qs = qs.filter(department_id=dept)
        if status == 'active':
            qs = qs.filter(is_active=True)
        elif status == 'inactive':
            qs = qs.filter(is_active=False)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['departments'] = Department.objects.filter(is_active=True)
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['selected_dept'] = self.request.GET.get('department', '')
        ctx['selected_status'] = self.request.GET.get('status', '')
        return ctx


class EmployeeDetailView(AdminRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['recent_reports'] = self.object.daily_reports.order_by('-date')[:10]
        ctx['total_reports'] = self.object.daily_reports.count()
        return ctx


class EmployeeCreateView(AdminRequiredMixin, CreateView):
    model = EmployeeProfile
    form_class = EmployeeCreateForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        log_activity(
            self.request.user, 'EMPLOYEE_ADDED',
            f"Employee '{self.object.full_name}' added.",
            get_client_ip(self.request),
        )
        send_notification(
            self.object.user,
            f"Welcome to the team, {self.object.full_name}! Your account has been created.",
            'success',
            '/dashboard/',
        )
        messages.success(self.request, f"Employee '{self.object.full_name}' created successfully.")
        return resp


class EmployeeUpdateView(AdminRequiredMixin, UpdateView):
    model = EmployeeProfile
    form_class = EmployeeEditForm
    template_name = 'employees/employee_form.html'

    def get_success_url(self):
        return reverse_lazy('employees:employee_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        resp = super().form_valid(form)
        log_activity(
            self.request.user, 'EMPLOYEE_EDITED',
            f"Employee '{self.object.full_name}' profile updated.",
            get_client_ip(self.request),
        )
        messages.success(self.request, f"Employee '{self.object.full_name}' updated.")
        return resp


class EmployeeDeleteView(AdminRequiredMixin, DeleteView):
    model = EmployeeProfile
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employees:employee_list')

    def form_valid(self, form):
        name = self.object.full_name
        user = self.object.user
        resp = super().form_valid(form)
        user.delete()
        log_activity(self.request.user, 'EMPLOYEE_DELETED', f"Employee '{name}' deleted.", get_client_ip(self.request))
        messages.success(self.request, f"Employee '{name}' deleted successfully.")
        return resp


class ResetEmployeePasswordView(AdminRequiredMixin, FormView):
    """Admin resets another employee's password."""

    template_name = 'employees/reset_employee_password.html'
    form_class = AdminResetPasswordForm

    def get_employee(self):
        return get_object_or_404(EmployeeProfile, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_employee().user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['employee'] = self.get_employee()
        return ctx

    def form_valid(self, form):
        form.save()
        employee = self.get_employee()
        log_activity(
            self.request.user, 'PASSWORD_RESET',
            f"Admin reset password for employee '{employee.full_name}'.",
            get_client_ip(self.request),
        )
        send_notification(
            employee.user,
            'Your password has been reset by an administrator.',
            'warning',
        )
        messages.success(self.request, f"Password for '{employee.full_name}' has been reset.")
        return redirect('employees:employee_detail', pk=employee.pk)


class EmployeeProfileSelfEditView(EmployeeRequiredMixin, UpdateView):
    """Employee edits their own profile."""

    model = EmployeeProfile
    form_class = EmployeeProfileSelfEditForm
    template_name = 'employees/profile_edit.html'
    success_url = reverse_lazy('dashboard:index')

    def get_object(self, queryset=None):
        return get_object_or_404(EmployeeProfile, user=self.request.user)

    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, 'Your profile has been updated.')
        return resp
