# Employee Daily Work Report Management System

A secure, responsive, and production-ready enterprise-grade Django web application for companies to manage daily work reports submitted by their employees. 

## Features

- **Role-Based Access Control (RBAC):** Two core roles: **Admin** (Staff) and **Employee** (Non-staff).
- **Secure Authentication:** Secure session-based authentication with Login, Logout, Change Password, and Password Reset (email-ready) features.
- **Dynamic Employee Dashboard:** Welcomes the employee, shows live local system clock, submission status, quick counters, a daily submission form with local character counting, and a log of recent submissions.
- **Submission Guardrails:** Limits report submissions to exactly **one report per employee per day** with server-side validation.
- **Admin Dashboard:** Provides real-time statistics (Total staff, reports today, pending submissions, monthly report trends) and Chart.js visualizations.
- **Employee & Department Management:** Full CRUD management of organizational departments, designations (dynamically filtered on form selection), and staff profiles.
- **Advanced Search and Filters:** Filter reports by named date ranges (Today, Yesterday, Last 7/30 Days, Current/Previous Month, Custom Date Range), department, specific employee, or content keyword.
- **Data Export Engine:** Allows Admins to export filtered report datasets directly to **PDF**, **Excel (.xlsx)**, or **CSV** formats, or view a **Print-Friendly** layout.
- **Audit Logs:** Automatically logs every important action (Logins, logouts, report creation/modification, employee additions, settings edits) along with timestamps and IP addresses.
- **Theme Engine:** Integrated persistence-backed light/dark mode switch.

---

## Technical Stack

- **Core:** Python 3.13+, Django 5/6
- **Package Management:** UV (using `pyproject.toml` and `uv.lock`)
- **Database:** SQLite (local development) / PostgreSQL ready (production configuration)
- **Frontend UI:** Bootstrap 5.3 (Vanilla CSS and Javascript), Bootstrap Icons, Chart.js
- **Exporting Engine:** ReportLab (PDF), openpyxl (Excel), white-noise (production assets)

---

## Project Folder Structure

```text
project/
├── apps/
│   ├── accounts/         # Login, logout, change password, password reset
│   ├── core/             # Base settings, mixins, middleware, activity log
│   ├── dashboard/        # Role-based landing dashboard routing & graphs
│   ├── employees/        # Departments, designations, employee profiles
│   ├── notifications/    # In-app notifications
│   └── reports/          # Daily reports submit, lists, exports
├── config/
│   ├── settings/
│   │   ├── base.py       # Shared configuration settings
│   │   ├── development.py# Dev configurations (SQLite, console email)
│   │   └── production.py # Prod configurations (PostgreSQL, SSL headers)
│   ├── urls.py           # Root URL routing
│   └── wsgi.py / asgi.py # Deployment handlers
├── static/
│   ├── css/style.css     # Clean corporate layout theme styles (Light/Dark mode)
│   └── js/app.js         # Theme toggles, character counts, live clocks, AJAX
├── templates/            # Django HTML templates organized by application
├── db.sqlite3            # Dev SQLite database
├── manage.py             # Management entry point
├── pyproject.toml        # Dependency declarations
├── uv.lock               # UV locked dependencies
└── README.md             # Project documentation
```

---

## Installation & Setup

Ensure you have **Python 3.13+** and **UV** installed on your system.

### 1. Project Sync
Initialize virtual environment and install all lockfile dependencies:
```bash
uv sync
```

### 2. Configure Environment Variables
Create a local `.env` configuration file in the project root:
```bash
cp .env.example .env
```
Fill out the variables inside `.env` (Timezones, security keys, database credentials).

### 3. Database Migration
Apply all database migrations:
```bash
uv run python manage.py migrate
```

### 4. Create Admin Account
Create a superuser to access the Admin dashboard:
```bash
uv run python manage.py createsuperuser
```

### 5. Running the Application
Start the development server:
```bash
uv run python manage.py runserver
```
Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Running Unit Tests

Run the complete test suite:
```bash
uv run python manage.py test apps.employees.tests apps.reports.tests
```

---

## Production Deployment Notes

1. **Environment Settings:** Set `DEBUG=False` in your `.env` file.
2. **Security Headers:** The `production.py` settings enable SSL redirection, HTTP Strict Transport Security (HSTS), and cookie flags. Ensure your production site runs on HTTPS.
3. **Database Configuration:** Configure PostgreSQL credentials in your `.env` file.
4. **Static Assets:** Collect all static assets prior to deploying:
   ```bash
   uv run python manage.py collectstatic
   ```
   WhiteNoise is pre-configured to compress and serve static files efficiently.

---

## Docker Setup

To run the application using Docker and Docker Compose (which spins up the Django web container and a PostgreSQL 15 database container):

### 1. Build and Run containers
```bash
docker-compose up --build -d
```

### 2. Create Superuser in container
```bash
docker-compose exec web python manage.py createsuperuser
```

### 3. Check logs
```bash
docker-compose logs -f
```

The system will automatically run database migrations, collect static files, and launch the server at `http://localhost:8000`.

