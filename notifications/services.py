from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification


class NotificationService:


    @staticmethod
    def send_notification(
        user,
        title,
        body,
        notification_type="system"
    ):

        notification = Notification.objects.create(
            recipient=user,
            title=title,
            body=body,
            notification_type=notification_type
        )


        channel_layer = get_channel_layer()


        async_to_sync(
            channel_layer.group_send
        )(
            f"user_{user.id}",
            {
                "type": "send_notification",
                "id": notification.id,
                "title": notification.title,
                "body": notification.body,
                "created_at": str(notification.created_at),
                "notification_type": notification.notification_type
            }
        )


        return notification