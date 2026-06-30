"""
Middleware for automatic activity logging on login/logout.
"""
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class ActivityLogMiddleware(MiddlewareMixin):
    """Captures the client IP for use in activity logs."""

    def process_request(self, request):
        request.client_ip = self._get_client_ip(request)

    @staticmethod
    def _get_client_ip(request) -> str:
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
