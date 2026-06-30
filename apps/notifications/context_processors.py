"""
Notifications context processor.
"""


def notifications_count(request) -> dict:
    """Inject unread notification count into every template context."""
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
    else:
        count = 0
    return {'unread_notifications_count': count}
