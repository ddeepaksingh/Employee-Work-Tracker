import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.reports.models import DailyReport, Activity, DailyReportActivity
from apps.employees.models import EmployeeProfile

print("=== Employees ===")
for emp in EmployeeProfile.objects.all():
    print(f"ID: {emp.id}, Employee ID: {emp.employee_id}, Full Name: {emp.full_name}, User: {emp.user.username}")

print("\n=== Activities ===")
for act in Activity.objects.all():
    print(f"ID: {act.id}, Name: {act.name}, Active: {act.is_active}")

print("\n=== Reports ===")
for r in DailyReport.objects.all():
    print(f"Report ID: {r.id}, Employee: {r.employee.full_name}, Date: {r.date}")
    print(f"Compiled Text:\n{r.report_text}")
    print("Associated Activities:")
    for ra in r.activities.all():
        print(f"  - Activity: {ra.activity.name}, Qty: {ra.quantity}, Text: {ra.report_text}")
    print("-" * 40)
