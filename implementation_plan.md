# Employee Daily Work Report Management System — Implementation Plan

## Overview

A complete, production-ready Django 5+ application for managing employee daily work reports. Built with UV as the package manager, Bootstrap 5 for UI, SQLite for development (PostgreSQL-ready), role-based access control, rich analytics, and export capabilities.

---

## Architecture Summary

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.x, Python 3.13+ |
| Package Manager | UV + pyproject.toml |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | Bootstrap 5.3, Vanilla JS, Chart.js |
| Auth | Django built-in + django-allauth (email ready) |
| PDF Export | ReportLab or WeasyPrint |
| Excel/CSV | openpyxl + csv module |
| Env Vars | python-decouple |
| Icons | Bootstrap Icons |

---

## Project Folder Structure

```
e:\Attendence\
├── config/                    # Django project settings package
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/              # Auth: login, logout, password
│   ├── employees/             # EmployeeProfile, Department, Designation
│   ├── reports/               # DailyReport CRUD
│   ├── dashboard/             # Role-aware dashboards
│   ├── notifications/         # Notifications model + views
│   └── core/                  # Mixins, utils, activity log, base views
├── templates/
│   ├── base.html
│   ├── partials/
│   ├── accounts/
│   ├── employees/
│   ├── reports/
│   ├── dashboard/
│   └── notifications/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/                     # Uploaded files
├── logs/                      # App log files
├── .env
├── .env.example
├── pyproject.toml
├── manage.py
└── README.md
```

---

## Database Models

### `apps/accounts` — User extension via EmployeeProfile (in employees app)
- Uses Django's built-in `User` model

### `apps/employees`
- **Department**: name, description, is_active, created_at
- **Designation**: name, department (FK), is_active, created_at
- **EmployeeProfile**: user (OneToOne), department (FK), designation (FK), employee_id, phone, avatar, date_joined, is_active

### `apps/reports`
- **DailyReport**: employee (FK→EmployeeProfile), report_text, date, created_at, updated_at, is_edited, word_count
- Unique constraint: (employee, date)

### `apps/notifications`
- **Notification**: recipient (FK→User), message, notification_type, is_read, created_at, link

### `apps/core`
- **ActivityLog**: user (FK), action, description, ip_address, timestamp, extra_data (JSON)

### `apps/core` — Settings
- **CompanySettings**: company_name, logo, timezone, date_format, submission_deadline, footer_text, theme

---

## Apps & Key Views

### `accounts`
- `LoginView` (custom, CSRF, rate-aware)
- `LogoutView`
- `ChangePasswordView`
- `ForgotPasswordView` (email-ready using Django's PasswordResetView)

### `dashboard`
- `EmployeeDashboardView` — shows today's status, quick stats, recent reports
- `AdminDashboardView` — shows KPI cards, charts, recent activity

### `employees` (Admin only)
- `EmployeeListView`, `EmployeeCreateView`, `EmployeeUpdateView`, `EmployeeDeleteView`
- `EmployeeDetailView`
- `DepartmentCRUD`, `DesignationCRUD`
- `ResetEmployeePasswordView`

### `reports`
- `ReportSubmitView` (Employee — one per day)
- `ReportHistoryView` (Employee — own reports only)
- `AdminReportListView`
- `AdminReportDetailView`
- `AdminReportEditView`
- `AdminReportDeleteView`
- `ExportReportsPDF`, `ExportReportsExcel`, `ExportReportsCSV`

### `notifications`
- `NotificationListView`
- `MarkReadView`

### `core`
- `ActivityLogListView` (Admin)
- `CompanySettingsView` (Admin)

---

## Role-Based Access

| Feature | Employee | Admin |
|---------|----------|-------|
| Dashboard | ✅ own | ✅ all |
| Submit Report | ✅ | ✅ |
| View Own Reports | ✅ | ✅ |
| View All Reports | ❌ | ✅ |
| Edit Any Report | ❌ | ✅ |
| Delete Report | ❌ | ✅ |
| Employee CRUD | ❌ | ✅ |
| Department/Designation CRUD | ❌ | ✅ |
| Export | ❌ | ✅ |
| Analytics | ❌ | ✅ |
| Activity Log | ❌ | ✅ |
| Settings | ❌ | ✅ |

---

## UI Design Plan

- Bootstrap 5.3 dark/light mode toggle
- Sidebar navigation (collapsible on mobile)
- KPI cards with icons (Bootstrap Icons)
- Chart.js for analytics (bar, line, doughnut)
- DataTables or custom paginated tables
- Toast notifications (Django messages → Bootstrap toasts)
- Confirmation modals for deletes
- Character counter on report textarea
- Loading spinner overlay
- Breadcrumbs on all inner pages
- Empty state illustrations for no-data scenarios

---

## Build Phases

### Phase 1 — Project Bootstrap
- UV init, pyproject.toml, install Django + dependencies
- Django project setup (config/, manage.py)
- Settings split (base/dev/prod)
- Environment variables (.env)

### Phase 2 — Core App + Models
- Create all Django apps
- Write all models with migrations
- Register models in admin
- ActivityLog + CompanySettings

### Phase 3 — Authentication
- Custom login/logout
- Password change & reset
- Session security

### Phase 4 — Base Templates + Static
- base.html with sidebar, topbar, footer
- Bootstrap 5 CDN + custom CSS
- Dark mode toggle JS
- Toast system

### Phase 5 — Employee App (Admin)
- Department/Designation CRUD
- Employee CRUD + profile management
- Admin employee dashboard

### Phase 6 — Reports App
- Employee report submission (one/day enforcement)
- Report history with filters & search
- Admin report management
- PDF/Excel/CSV export

### Phase 7 — Dashboards + Analytics
- Employee dashboard with live clock, status
- Admin dashboard with Chart.js
- Analytics views

### Phase 8 — Notifications + Activity Log
- Notification model + views
- Activity log capture on key actions
- Admin activity log list

### Phase 9 — Settings + README
- CompanySettings CRUD for admin
- README.md (professional)
- .env.example

---

## Dependencies (pyproject.toml)

```toml
[project]
name = "employee-report-system"
version = "1.0.0"
requires-python = ">=3.13"
dependencies = [
    "django>=5.0",
    "python-decouple>=3.8",
    "pillow>=10.0",          # image uploads
    "openpyxl>=3.1",         # Excel export
    "reportlab>=4.0",        # PDF export
    "django-crispy-forms>=2.1",
    "crispy-bootstrap5>=0.7",
    "psycopg2-binary>=2.9",  # PostgreSQL (optional for prod)
    "whitenoise>=6.6",       # static files in prod
]
```

---

## Verification Plan

1. `uv sync` — installs all dependencies cleanly
2. `uv run python manage.py migrate` — all migrations apply
3. `uv run python manage.py createsuperuser` — creates admin
4. `uv run python manage.py runserver` — server starts
5. Login as admin → verify dashboard, employee CRUD, report management, exports
6. Create employee user → verify employee dashboard, report submission, history

---

## Open Questions

> [!NOTE]
> The following are minor decisions made for you. Review if you'd like to change any:
> - **Logo**: A default placeholder logo will be included in `static/images/`
> - **Email backend**: Configured for console (dev). SMTP settings commented in `.env.example` for production
> - **Report character limit**: Min 50 chars, Max 5000 chars
> - **Submission deadline**: Default 11:59 PM (configurable in Settings)
> - **Timezone**: Default Asia/Kolkata (IST) — configurable
