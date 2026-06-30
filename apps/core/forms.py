"""
Core app forms: CompanySettings.
"""
from django import forms
from .models import CompanySettings


class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = ['company_name', 'company_logo', 'timezone', 'date_format', 'submission_deadline', 'footer_text', 'theme']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_company_name'}),
            'company_logo': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_company_logo'}),
            'timezone': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_timezone'}),
            'date_format': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_date_format'}),
            'submission_deadline': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'id_deadline'}),
            'footer_text': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_footer'}),
            'theme': forms.Select(attrs={'class': 'form-select', 'id': 'id_theme'}),
        }
