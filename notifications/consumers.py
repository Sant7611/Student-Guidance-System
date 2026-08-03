import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        # Reject unauthenticated users
        if self.user.is_anonymous:
            await self.close()
            return

        # Each user gets their own private notification room
        self.group_name = f"user_{self.user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            "event": "connection",
            "message": "WebSocket connected successfully"
        }))


    async def disconnect(self, close_code):

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )


    async def send_notification(self, event):

        await self.send(text_data=json.dumps({
            "event": "notification",
            "data": {
                "id": event["id"],
                "title": event["title"],
                "body": event["body"],
                "created_at": event["created_at"],
                "is_read": event.get("is_read", False),
            }
        }))