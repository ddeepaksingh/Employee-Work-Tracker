"""
Reports app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Employee
    path('submit/', views.ReportSubmitView.as_view(), name='report_submit'),
    path('history/', views.ReportHistoryView.as_view(), name='report_history'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),

    # Admin
    path('admin/', views.AdminReportListView.as_view(), name='admin_report_list'),
    path('admin/<int:pk>/', views.AdminReportDetailView.as_view(), name='admin_report_detail'),
    path('admin/<int:pk>/edit/', views.AdminReportEditView.as_view(), name='admin_report_edit'),
    path('admin/<int:pk>/delete/', views.AdminReportDeleteView.as_view(), name='admin_report_delete'),

    # Exports
    path('export/csv/', views.ExportReportsCSVView.as_view(), name='export_csv'),
    path('export/excel/', views.ExportReportsExcelView.as_view(), name='export_excel'),
    path('export/pdf/', views.ExportReportsPDFView.as_view(), name='export_pdf'),
]
