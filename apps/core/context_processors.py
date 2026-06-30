"""
Template context processors for core app.
"""
from apps.core.models import CompanySettings


def company_settings(request) -> dict:
    """Inject company settings into every template context."""
    settings_obj = CompanySettings.get_settings()
    return {'company_settings': settings_obj}
