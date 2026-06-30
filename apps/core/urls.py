"""
Core app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('activity-log/', views.ActivityLogListView.as_view(), name='activity_log'),
    path('settings/', views.CompanySettingsView.as_view(), name='settings'),
]
