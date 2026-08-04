from rest_framework import viewsets
from course.serializers.course_batch_serializer import CourseBatchSerializer
from course.models import CourseBatch
from utils.permissions import AdminOnlyPost
from notifications.services import NotificationService
from django.core.cache import cache

class CourseBatchView(viewsets.ModelViewSet):
    permission_classes = [AdminOnlyPost]
    serializer_class = CourseBatchSerializer
    queryset = CourseBatch.objects.all().select_related('course')
    ordering = ["-created_at"]

    def _invalidate_batch_caches(self, instance, extra_mentor_id=None):
        # Any change to a batch (schedule, dates, mentor, status...) has to bust
        # the mentor's dashboard cache AND every enrolled student's dashboard
        # cache, since StudentEnrollmentSerializer nests the batch (with its
        # schedule) inside student_dashboard's cached response.
        if instance.mentor_id:
            cache.delete(f"mentor_dashboard:{instance.mentor_id}")
        if extra_mentor_id and extra_mentor_id != instance.mentor_id:
            cache.delete(f"mentor_dashboard:{extra_mentor_id}")
        student_ids = instance.enrollments.filter(is_deleted=False).values_list('student_id', flat=True)
        for student_id in student_ids:
            cache.delete(f"student_dashboard:{student_id}")

    def perform_create(self, serializer):
        serializer.save()
        
        cache.delete(f"mentor_dashboard:{serializer.instance.mentor_id}")

        NotificationService.send_notification(
            user=self.request.user,
            title="New Course Batch Created",
            body=f"A new course batch has been created: {serializer.instance.course.title}.",
            notification_type="system",
        )
        
        #mentor notification
        NotificationService.send_notification(
            user=serializer.instance.mentor,
            title="You've been assigned to a new course batch",
            body=f"You have been assigned to the course batch: {serializer.instance.course.title}.",
            notification_type="system",
        )

    def perform_update(self, serializer):
        previous_mentor_id = serializer.instance.mentor_id
        instance = serializer.save()
        self._invalidate_batch_caches(instance, extra_mentor_id=previous_mentor_id)

    def perform_destroy(self, instance):
        self._invalidate_batch_caches(instance)
        instance.delete()
