from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.employees.models import Department, Designation, EmployeeProfile

User = get_user_model()


class EmployeeManagementTestCase(TestCase):
    """Test suite for organizational departments, designations, and employee profiles."""

    def setUp(self):
        # Create standard employee user
        self.employee_user = User.objects.create_user(
            username="employee_jane",
            email="jane@company.com",
            password="janepassword123",
            first_name="Jane",
            last_name="Doe"
        )
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username="admin_boss",
            email="boss@company.com",
            password="bosspassword123"
        )

        # Create department & designation
        self.dept = Department.objects.create(name="Human Resources", description="HR Department")
        self.desig = Designation.objects.create(name="HR Specialist", department=self.dept)

    def test_department_employee_count(self):
        """Test department headcount calculations."""
        profile = EmployeeProfile.objects.create(
            user=self.employee_user,
            department=self.dept,
            designation=self.desig,
            is_active=True
        )
        self.assertEqual(self.dept.employee_count, 1)

    def test_admin_access_employee_list(self):
        """Verify that admins can view the employee list page."""
        client = Client()
        client.login(username="admin_boss", password="bosspassword123")
        url = reverse("employees:employee_list")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_employee_denied_access_employee_list(self):
        """Verify that regular employees are redirected and denied access to employee lists."""
        client = Client()
        client.login(username="employee_jane", password="janepassword123")
        url = reverse("employees:employee_list")
        response = client.get(url)
        # Should redirect to employee dashboard with message
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard/", response.url)
