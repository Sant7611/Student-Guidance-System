from rest_framework import viewsets
from career.models import Career
from career.serializers import career_serializer
from utils.permissions import AdminOnlyPost
from notifications.services import NotificationService

class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    permission_classes = [AdminOnlyPost]
    ordering=['-created_at']

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return career_serializer.CareerReadSerializer
        return career_serializer.CareerCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        
        NotificationService.send_notification(
            user=self.request.user,
            title="New Career Opportunity",
            body=f"A new career opportunity has been posted: {serializer.instance.title}.",
            notification_type="system",
        )