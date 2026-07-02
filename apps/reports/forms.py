"""
Reports app forms.
"""
from django import forms
from django.conf import settings
from .models import DailyReport


from .models import DailyReport, Activity, DailyReportActivity


class ActivityForm(forms.ModelForm):
    """Form for admins to create and manage activities."""

    class Meta:
        model = Activity
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_activity_name', 'placeholder': 'e.g. NOPR'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'id_activity_desc', 'placeholder': 'Describe this activity...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_activity_active'}),
        }


class DailyReportForm(forms.ModelForm):
    """Form for employees to submit their daily report (metadata/shell form)."""

    class Meta:
        model = DailyReport
        fields = []


class AdminReportEditForm(forms.ModelForm):
    """Admin edit form for any daily report (metadata/date only)."""

    class Meta:
        model = DailyReport
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_admin_report_date'}),
        }



class ReportFilterForm(forms.Form):
    """Filter form for report lists."""

    RANGE_CHOICES = [
        ('', 'All Time'),
        ('today', 'Today'),
        ('yesterday', 'Yesterday'),
        ('week', 'Last 7 Days'),
        ('month', 'Last 30 Days'),
        ('current_month', 'Current Month'),
        ('prev_month', 'Previous Month'),
        ('custom', 'Custom Range'),
    ]

    date_range = forms.ChoiceField(
        choices=RANGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_filter_range'}),
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_filter_from'}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_filter_to'}),
    )
    department = forms.IntegerField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_filter_dept'}),
    )
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by keyword...',
            'id': 'id_filter_keyword',
        }),
    )
    employee = forms.IntegerField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_filter_employee'}),
    )
