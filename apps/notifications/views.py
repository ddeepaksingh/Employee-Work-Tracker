"""
Notifications app views.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, View
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user).order_by('-created_at')
        # Mark all as read when the list page is visited
        qs.filter(is_read=False).update(is_read=True)
        return qs


class MarkNotificationReadView(LoginRequiredMixin, View):
    """AJAX endpoint to mark a single notification as read."""

    def post(self, request, pk, *args, **kwargs):
        try:
            notif = Notification.objects.get(pk=pk, recipient=request.user)
            notif.mark_read()
            return JsonResponse({'status': 'ok'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)


class MarkAllReadView(LoginRequiredMixin, View):
    """Mark all of the user's notifications as read."""

    def post(self, request, *args, **kwargs):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        from django.shortcuts import redirect
        return redirect('notifications:notification_list')
