"""
Development settings — DEBUG mode, console email, SQLite.
"""
from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ['*']

# Use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}

# Django Debug Toolbar (optional — only if installed)
INTERNAL_IPS = ['127.0.0.1']
