from rest_framework import viewsets
from skill.models import Skill
from skill.serializers.skill_serializer import SkillDetailSerializer, SkillCreateSerializer
from rest_framework.permissions import AllowAny
from notifications.services import NotificationService

class SkillViewSet(viewsets.ModelViewSet):
    permission_classes =[AllowAny]
    queryset = Skill.objects.all()
    ordering=['-created_at']
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return SkillCreateSerializer
        return SkillDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        
        NotificationService.send_notification(
            user=self.request.user,
            title="New Skill Created",
            body=f"A new skill has been created: {serializer.instance.name}.",
            notification_type="system",
        )