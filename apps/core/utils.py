"""
Utility functions shared across apps.
"""
import logging
from typing import Optional
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


def log_activity(
    user,
    action: str,
    description: str = '',
    ip_address: Optional[str] = None,
    extra_data: Optional[dict] = None,
) -> None:
    """Create an ActivityLog entry. Silently handles errors to avoid breaking requests."""
    from apps.core.models import ActivityLog
    try:
        ActivityLog.objects.create(
            user=user,
            action=action,
            description=description,
            ip_address=ip_address,
            extra_data=extra_data or {},
        )
    except Exception as exc:
        logger.error("Failed to write activity log: %s", exc)


def get_client_ip(request) -> str:
    """Extract the real client IP from a request object."""
    return getattr(request, 'client_ip', request.META.get('REMOTE_ADDR', ''))


def send_notification(recipient, message: str, notification_type: str = 'info', link: str = '') -> None:
    """Create an in-app notification for a user."""
    from apps.notifications.models import Notification
    try:
        Notification.objects.create(
            recipient=recipient,
            message=message,
            notification_type=notification_type,
            link=link,
        )
    except Exception as exc:
        logger.error("Failed to send notification: %s", exc)
