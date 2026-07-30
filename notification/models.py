from django.db import models
from base.models import BaseModel


class Notification(BaseModel):
    """
    Notification model to store notifications for users.
    """
    recipent = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipent.username}: {self.title}"