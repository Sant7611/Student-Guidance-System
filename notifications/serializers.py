from rest_framework import serializers

from .models import Notification
from utils.response_helpers import error_response, success_response

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'body', 'is_read', 'created_at', 'notification_type']

    def post(self, request, *args, **kwargs):
        msg={
            'error': 'This is not allowed'
        }
        return error_response(message=msg, status=400)