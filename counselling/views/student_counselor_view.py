from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from counselling.models import StudentCounselor
from counselling.serializers.student_counselor_serializer import StudentCounselorReadSerializer, StudentCounselorWriteSerializer
from notifications.services import NotificationService


class StudentCounselorViewSet(viewsets.ModelViewSet):
    queryset = StudentCounselor.objects.all()
    permission_classes = [IsAuthenticated]
    ordering=['-created_at']

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return StudentCounselorReadSerializer
        return StudentCounselorWriteSerializer

    def _invalidate_dashboards(self, instance):
        cache.delete(f"student_dashboard:{instance.student_id}")
        cache.delete(f"counselor_dashboard:{instance.counselor_id}")

    def perform_create(self, serializer):
        serializer.save()
        self._invalidate_dashboards(serializer.instance)

        #for counselor notification
        NotificationService.send_notification(
            user=serializer.instance.counselor,
            title="You've been assigned a new student",
            body=f"A new student has been assigned to you: {serializer.instance.student.username}.",
            notification_type="system",
        )
        
        
        #for student notification
        NotificationService.send_notification(
            user=serializer.instance.student,
            title="You've been assigned a new counselor",
            body=f"A new counselor has been assigned to you: {serializer.instance.counselor.username}.",
            notification_type="system",
        )

    def perform_update(self, serializer):
        serializer.save()
        self._invalidate_dashboards(serializer.instance)

    def perform_destroy(self, instance):
        self._invalidate_dashboards(instance)
        instance.delete()
