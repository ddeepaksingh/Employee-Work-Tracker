"""
Accounts app forms: Login, ChangePassword.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class CustomLoginForm(AuthenticationForm):
    """Styled login form using Bootstrap 5."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Username or Email',
            'autofocus': True,
            'id': 'id_login_username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Password',
            'id': 'id_login_password',
        })
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    """Styled password change form."""

    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_old_password'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_new_password1'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_new_password2'})
    )
