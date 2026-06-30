from datetime import date, timedelta
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from apps.employees.models import Department, Designation, EmployeeProfile
from apps.reports.models import DailyReport

User = get_user_model()


class DailyReportTestCase(TestCase):
    """Test suite for the DailyReport model and submission rules."""

    def setUp(self):
        # Setup department and designation
        self.dept = Department.objects.create(name="Engineering", description="Software Dev team")
        self.desig = Designation.objects.create(name="Software Engineer", department=self.dept)

        # Create user & employee profile
        self.user = User.objects.create_user(
            username="john_doe",
            email="john@company.com",
            password="securepassword123",
            first_name="John",
            last_name="Doe"
        )
        self.profile = EmployeeProfile.objects.create(
            user=self.user,
            department=self.dept,
            designation=self.desig,
            phone="1234567890",
            is_active=True
        )

        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username="admin_user",
            email="admin@company.com",
            password="adminpassword123"
        )

    def test_report_creation(self):
        """Test standard daily report creation and automatic calculations."""
        report = DailyReport.objects.create(
            employee=self.profile,
            date=date.today(),
            report_text="Completed project setup. Configured database routing and written initial model tests today."
        )
        self.assertEqual(report.word_count, 12)
        self.assertFalse(report.is_edited)
        self.assertEqual(str(report), f"{self.profile.full_name} — {date.today()}")

    def test_single_report_per_day_constraint(self):
        """Verify that an employee cannot submit more than one report on the same day."""
        DailyReport.objects.create(
            employee=self.profile,
            date=date.today(),
            report_text="This is report number one. Today I finished tasks A, B, and C."
        )
        
        # Creating a second report for the same employee on the same day should raise an integrity error or validation error
        with self.assertRaises(Exception):
            DailyReport.objects.create(
                employee=self.profile,
                date=date.today(),
                report_text="This is report number two. Today I finished task D."
            )

    def test_report_on_different_days(self):
        """Verify that an employee can submit reports on different days."""
        report_yesterday = DailyReport.objects.create(
            employee=self.profile,
            date=date.today() - timedelta(days=1),
            report_text="This is yesterday's report. Completed tasks and verified settings."
        )
        report_today = DailyReport.objects.create(
            employee=self.profile,
            date=date.today(),
            report_text="This is today's report. Completed tasks and verified settings."
        )
        self.assertEqual(DailyReport.objects.filter(employee=self.profile).count(), 2)

    def test_submission_view_authenticated(self):
        """Test report submission via HTTP post by authenticated employee."""
        client = Client()
        client.login(username="john_doe", password="securepassword123")
        
        url = reverse("reports:report_submit")
        response = client.post(url, {
            "report_text": "Successfully worked on the login view and fixed the routing issue. Tested settings locally."
        })
        # Should redirect to index upon success
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DailyReport.objects.filter(employee=self.profile).count(), 1)

    def test_submission_view_unauthenticated(self):
        """Test report submission redirects to login for unauthenticated visitors."""
        client = Client()
        url = reverse("reports:report_submit")
        response = client.post(url, {
            "report_text": "Unauthenticated report text."
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
        self.assertEqual(DailyReport.objects.count(), 0)
