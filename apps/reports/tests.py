from datetime import date, timedelta
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.employees.models import Department, Designation, EmployeeProfile
from apps.reports.models import DailyReport, Activity, DailyReportActivity

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

        # Create standard activities
        self.act1 = Activity.objects.create(name="NOPR", description="National Open Paper Repository")
        self.act2 = Activity.objects.create(name="NKRC", description="National Knowledge Resource Consortium")

    def test_report_creation_fallback(self):
        """Test fallback/direct daily report creation for backwards compatibility."""
        report = DailyReport.objects.create(
            employee=self.profile,
            date=date.today(),
            report_text="Completed project setup. Configured database routing and written initial model tests today."
        )
        self.assertEqual(report.word_count, 12)
        self.assertFalse(report.is_edited)
        self.assertEqual(str(report), f"{self.profile.full_name} — {date.today()}")

    def test_report_creation_with_activities(self):
        """Test report creation with multiple activity entries and compilation of report_text."""
        report = DailyReport.objects.create(
            employee=self.profile,
            date=date.today(),
        )
        DailyReportActivity.objects.create(
            daily_report=report,
            activity=self.act1,
            report_text="Uploaded 10 research papers.",
            quantity=10
        )
        DailyReportActivity.objects.create(
            daily_report=report,
            activity=self.act2,
            report_text="Verified metadata for journal records.",
            quantity=5
        )
        # Calling save compiles report_text and calculates word count
        report.save()

        expected_text = (
            f"Activity: NOPR\nQuantity: 10\nReport: Uploaded 10 research papers.\n\n"
            f"---\n\n"
            f"Activity: NKRC\nQuantity: 5\nReport: Verified metadata for journal records."
        )
        self.assertEqual(report.report_text, expected_text)
        self.assertTrue(report.word_count > 0)

    def test_single_report_per_day_constraint(self):
        """Verify that an employee cannot submit more than one report on the same day."""
        DailyReport.objects.create(
            employee=self.profile,
            date=date.today(),
            report_text="This is report number one. Today I finished tasks A, B, and C."
        )
        
        # Creating a second report for the same employee on the same day should raise an integrity error
        with self.assertRaises(Exception):
            DailyReport.objects.create(
                employee=self.profile,
                date=date.today(),
                report_text="This is report number two. Today I finished task D."
            )

    def test_report_on_different_days(self):
        """Verify that an employee can submit reports on different days."""
        DailyReport.objects.create(
            employee=self.profile,
            date=date.today() - timedelta(days=1),
            report_text="This is yesterday's report. Completed tasks and verified settings."
        )
        DailyReport.objects.create(
            employee=self.profile,
            date=date.today(),
            report_text="This is today's report. Completed tasks and verified settings."
        )
        self.assertEqual(DailyReport.objects.filter(employee=self.profile).count(), 2)

    def test_submission_view_authenticated(self):
        """Test report submission via HTTP post by authenticated employee using multi-activities."""
        client = Client()
        client.login(username="john_doe", password="securepassword123")
        
        url = reverse("reports:report_submit")
        response = client.post(url, {
            "activity": [str(self.act1.id), str(self.act2.id)],
            "report": ["Uploaded 10 research papers.", "Verified metadata for journal records."],
            "quantity": ["10", "5"]
        })
        # Should redirect to dashboard upon success
        self.assertEqual(response.status_code, 302)
        
        report = DailyReport.objects.filter(employee=self.profile).first()
        self.assertIsNotNone(report)
        self.assertEqual(report.activities.count(), 2)
        self.assertIn("Activity: NOPR", report.report_text)
        self.assertIn("Activity: NKRC", report.report_text)

    def test_submission_view_unauthenticated(self):
        """Test report submission redirects to login for unauthenticated visitors."""
        client = Client()
        url = reverse("reports:report_submit")
        response = client.post(url, {
            "activity": [str(self.act1.id)],
            "report": ["Unauthenticated report text."],
            "quantity": ["1"]
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
        self.assertEqual(DailyReport.objects.count(), 0)
