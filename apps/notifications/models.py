"""
Notifications app models.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    """In-app notification for a user."""

    TYPE_CHOICES = [
        ('info', 'Info'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
        ('reminder', 'Reminder'),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='info',
    )
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self) -> str:
        return f"[{self.notification_type}] {self.recipient.username}: {self.message[:50]}"

    def mark_read(self) -> None:
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
