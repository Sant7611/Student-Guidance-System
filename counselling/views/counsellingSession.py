from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from counselling.models import CounselingSession
from counselling.serializers.CounsellingSessionSerializer import CounselingSessionReadSerializer, CounselingSessionWriteSerializer


class CounselingSessionViewSet(viewsets.ModelViewSet):
    queryset = CounselingSession.objects.all().select_related('student_counselor')
    permission_classes = [IsAuthenticated]
    ordering=['-created_at']

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return CounselingSessionReadSerializer
        return CounselingSessionWriteSerializer

    def _invalidate_dashboards(self, instance):
        # The student/counselor dashboards cache their "schedule" data for 5 minutes
        # (see dashboard/views/*), so any session change has to bust both caches
        # immediately or the change won't show up until the cache expires.
        cache.delete(f"student_dashboard:{instance.student_counselor.student_id}")
        cache.delete(f"counselor_dashboard:{instance.student_counselor.counselor_id}")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._invalidate_dashboards(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._invalidate_dashboards(instance)

    def perform_destroy(self, instance):
        self._invalidate_dashboards(instance)
        instance.delete()
