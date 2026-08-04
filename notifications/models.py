from django.conf import settings
from django.db import models


class Notification(models.Model):
    
    class NotificationType(models.TextChoices):
        SYSTEM = 'system', 'System'
        MESSAGE = 'message', 'Message'
        ALERT = 'alert', 'Alert'
        REMINDER = 'reminder', 'Reminder'
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50, default='system', choices=NotificationType.choices)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} -> {self.recipient}"
