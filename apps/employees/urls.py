"""
Employees app URL configuration.
"""
from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    # Employee profile (self)
    path('profile/edit/', views.EmployeeProfileSelfEditView.as_view(), name='profile_edit'),

    # Employee management (admin)
    path('', views.EmployeeListView.as_view(), name='employee_list'),
    path('add/', views.EmployeeCreateView.as_view(), name='employee_add'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('<int:pk>/reset-password/', views.ResetEmployeePasswordView.as_view(), name='reset_password'),

    # Department management
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/add/', views.DepartmentCreateView.as_view(), name='department_add'),
    path('departments/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_edit'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),

    # Designation management
    path('designations/', views.DesignationListView.as_view(), name='designation_list'),
    path('designations/add/', views.DesignationCreateView.as_view(), name='designation_add'),
    path('designations/<int:pk>/edit/', views.DesignationUpdateView.as_view(), name='designation_edit'),
    path('designations/<int:pk>/delete/', views.DesignationDeleteView.as_view(), name='designation_delete'),
]
