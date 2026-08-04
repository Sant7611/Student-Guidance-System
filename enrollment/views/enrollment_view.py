from rest_framework import viewsets
from django.core.cache import cache
from enrollment.models import Enrollment
from enrollment.serializers.enrollment_serializer import  EnrollmentCreateSerializer, EnrollmentDetailSerializer
from rest_framework.permissions import IsAdminUser
from notifications.services import NotificationService

class EnrollmentView(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'batch', 'batch__mentor', "batch__course")
    permission_classes=[IsAdminUser]
    ordering=['-created_at']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EnrollmentCreateSerializer
        return EnrollmentDetailSerializer

    def _invalidate_dashboards(self, instance):
        cache.delete(f"student_dashboard:{instance.student_id}")
        if instance.batch and instance.batch.mentor_id:
            cache.delete(f"mentor_dashboard:{instance.batch.mentor_id}")

    def perform_create(self, serializer):
        enrollment = serializer.save()
        self._invalidate_dashboards(enrollment)

        NotificationService.send_notification(
            user=enrollment.student,
            title="Enrollment Successful",
            body=f"You have successfully enrolled in {enrollment.batch.course.title}.",
            notification_type="enrollment",
        )

    def perform_update(self, serializer):
        enrollment = serializer.save()
        self._invalidate_dashboards(enrollment)

    def perform_destroy(self, instance):
        self._invalidate_dashboards(instance)
        instance.delete()