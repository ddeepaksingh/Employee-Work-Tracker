"""
Root URL configuration for the project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('employees/', include('apps.employees.urls', namespace='employees')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('core/', include('apps.core.urls', namespace='core')),
    # Root redirect
    path('', lambda request: redirect('dashboard/', permanent=False)),
]

# Serve media files (in development, and in production for local network use without Nginx)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Admin site customisation
admin.site.site_header = 'Employee Report System'
admin.site.site_title = 'ERS Admin'
admin.site.index_title = 'Administration'
