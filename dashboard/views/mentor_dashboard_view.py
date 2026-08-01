from rest_framework import generics
from utils.response_helpers import success_response, error_response
from course.models import CourseBatch
from enrollment.models import Enrollment
from dashboard.serializers.mentor_dashboard_serilaizer import MentorBatchSerializer
from django.db.models import Prefetch
from utils.permissions import IsOwner
from django.core.cache import cache

class MentorDashboardView(generics.GenericAPIView):
    permission_classes = [IsOwner]

    def get(self, request):
        if request.user.role != "mentor":
            return error_response(message="Unauthorized access", status_code=403)

        mentor = request.user

        base_key = f"mentor_dashboard:{mentor.id}"
        cached_data = cache.get(base_key)
        if cached_data is not None:
            return success_response(data=cached_data, status_code=200)
        
        batches = (
            CourseBatch.objects.filter(mentor=mentor)
            .select_related("course")
            .prefetch_related(
                Prefetch(
                    "enrollments", queryset=Enrollment.objects.select_related("student")
                )
            )
        )
        batches = MentorBatchSerializer(batches, many=True)

        cache.set(base_key, {"batches": batches.data}, 300)

        return success_response(data={"batches": batches.data}, status_code=200)
