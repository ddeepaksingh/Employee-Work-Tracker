"""
Reports app forms.
"""
from django import forms
from django.conf import settings
from .models import DailyReport


class DailyReportForm(forms.ModelForm):
    """Form for employees to submit their daily report."""

    class Meta:
        model = DailyReport
        fields = ['report_text']
        widgets = {
            'report_text': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'id_report_text',
                'rows': 12,
                'placeholder': 'Describe your work activities for today in detail...',
                'minlength': getattr(settings, 'REPORT_MIN_LENGTH', 50),
                'maxlength': getattr(settings, 'REPORT_MAX_LENGTH', 5000),
            }),
        }
        labels = {'report_text': 'Today\'s Work Report'}

    def clean_report_text(self):
        text = self.cleaned_data.get('report_text', '').strip()
        min_len = getattr(settings, 'REPORT_MIN_LENGTH', 50)
        max_len = getattr(settings, 'REPORT_MAX_LENGTH', 5000)
        if len(text) < min_len:
            raise forms.ValidationError(f'Report must be at least {min_len} characters long.')
        if len(text) > max_len:
            raise forms.ValidationError(f'Report cannot exceed {max_len} characters.')
        return text


class AdminReportEditForm(forms.ModelForm):
    """Admin edit form for any daily report."""

    class Meta:
        model = DailyReport
        fields = ['report_text', 'date']
        widgets = {
            'report_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 12, 'id': 'id_admin_report_text'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_admin_report_date'}),
        }

    def clean_report_text(self):
        text = self.cleaned_data.get('report_text', '').strip()
        if len(text) < 10:
            raise forms.ValidationError('Report is too short.')
        return text


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
