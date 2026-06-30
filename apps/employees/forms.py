"""
Employee app forms: Department, Designation, EmployeeProfile, EditProfile.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from .models import Department, Designation, EmployeeProfile

User = get_user_model()

_input = lambda extra='': f'form-control {extra}'.strip()
_select = 'form-select'
_check = 'form-check-input'


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': _input(), 'id': 'id_dept_name'}),
            'description': forms.Textarea(attrs={'class': _input(), 'rows': 3, 'id': 'id_dept_desc'}),
            'is_active': forms.CheckboxInput(attrs={'class': _check, 'id': 'id_dept_active'}),
        }


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name', 'department', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': _input(), 'id': 'id_desig_name'}),
            'department': forms.Select(attrs={'class': _select, 'id': 'id_desig_dept'}),
            'is_active': forms.CheckboxInput(attrs={'class': _check, 'id': 'id_desig_active'}),
        }


class EmployeeCreateForm(forms.ModelForm):
    """Creates a new Django User alongside the EmployeeProfile."""

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': _input(), 'id': 'id_emp_first_name'}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': _input(), 'id': 'id_emp_last_name'}),
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': _input(), 'id': 'id_emp_username'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': _input(), 'id': 'id_emp_email'}),
    )
    password = forms.CharField(
        label='Initial Password',
        widget=forms.PasswordInput(attrs={'class': _input(), 'id': 'id_emp_password'}),
    )

    class Meta:
        model = EmployeeProfile
        fields = ['department', 'designation', 'employee_id', 'phone', 'avatar', 'date_of_joining', 'is_active']
        widgets = {
            'department': forms.Select(attrs={'class': _select, 'id': 'id_emp_dept'}),
            'designation': forms.Select(attrs={'class': _select, 'id': 'id_emp_desig'}),
            'employee_id': forms.TextInput(attrs={'class': _input(), 'id': 'id_emp_id', 'placeholder': 'Auto-generated if empty'}),
            'phone': forms.TextInput(attrs={'class': _input(), 'id': 'id_emp_phone'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_emp_avatar'}),
            'date_of_joining': forms.DateInput(attrs={'class': _input(), 'type': 'date', 'id': 'id_emp_doj'}),
            'is_active': forms.CheckboxInput(attrs={'class': _check, 'id': 'id_emp_active'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with this username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        profile.user = user
        if commit:
            profile.save()
        return profile


class EmployeeEditForm(forms.ModelForm):
    """Edits an existing employee's user and profile data."""

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': _input(), 'id': 'id_edit_first_name'}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': _input(), 'id': 'id_edit_last_name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': _input(), 'id': 'id_edit_email'}),
    )

    class Meta:
        model = EmployeeProfile
        fields = ['department', 'designation', 'employee_id', 'phone', 'avatar', 'date_of_joining', 'is_active']
        widgets = {
            'department': forms.Select(attrs={'class': _select, 'id': 'id_edit_dept'}),
            'designation': forms.Select(attrs={'class': _select, 'id': 'id_edit_desig'}),
            'employee_id': forms.TextInput(attrs={'class': _input(), 'id': 'id_edit_emp_id'}),
            'phone': forms.TextInput(attrs={'class': _input(), 'id': 'id_edit_phone'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_edit_avatar'}),
            'date_of_joining': forms.DateInput(attrs={'class': _input(), 'type': 'date', 'id': 'id_edit_doj'}),
            'is_active': forms.CheckboxInput(attrs={'class': _check, 'id': 'id_edit_active'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile


class EmployeeProfileSelfEditForm(forms.ModelForm):
    """Allows an employee to edit their own non-sensitive profile fields."""

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': _input(), 'id': 'id_self_first_name'}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': _input(), 'id': 'id_self_last_name'}),
    )

    class Meta:
        model = EmployeeProfile
        fields = ['phone', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': _input(), 'id': 'id_self_phone'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_self_avatar'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile.save()
        return profile


class AdminResetPasswordForm(SetPasswordForm):
    """Admin resets an employee password."""

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': _input(), 'id': 'id_reset_pw1'}),
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': _input(), 'id': 'id_reset_pw2'}),
    )
