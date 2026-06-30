"""
Accounts app views: Login, Logout, ChangePassword, PasswordReset.
"""
import logging
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from apps.core.utils import log_activity, get_client_ip
from .forms import CustomLoginForm, CustomPasswordChangeForm

logger = logging.getLogger(__name__)


class CustomLoginView(FormView):
    """Handles user login with session management."""

    template_name = 'accounts/login.html'
    form_class = CustomLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        remember = form.cleaned_data.get('remember_me', False)
        login(self.request, user)

        if not remember:
            self.request.session.set_expiry(0)

        log_activity(
            user=user,
            action='LOGIN',
            description=f"User '{user.username}' logged in.",
            ip_address=get_client_ip(self.request),
        )
        logger.info("User '%s' logged in from %s", user.username, get_client_ip(self.request))
        messages.success(self.request, f"Welcome back, {user.get_full_name() or user.username}!")

        next_url = self.request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('dashboard:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class CustomLogoutView(LoginRequiredMixin, View):
    """Logs out the user and redirects to login page."""

    def post(self, request, *args, **kwargs):
        log_activity(
            user=request.user,
            action='LOGOUT',
            description=f"User '{request.user.username}' logged out.",
            ip_address=get_client_ip(request),
        )
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('accounts:login')


class ChangePasswordView(LoginRequiredMixin, FormView):
    """Allows authenticated users to change their password."""

    template_name = 'accounts/change_password.html'
    form_class = CustomPasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        log_activity(
            user=self.request.user,
            action='PASSWORD_CHANGED',
            description='Password changed via profile.',
            ip_address=get_client_ip(self.request),
        )
        messages.success(self.request, 'Your password has been changed successfully.')
        return redirect('dashboard:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


# ── Password Reset (built-in Django views with custom templates) ───────────────

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
