from rest_framework import generics
from django.db.models import Prefetch
from django.utils import timezone
from counselling.models import StudentCounselor, CounselingSession
from dashboard.serializers.counselor_dashboard_serializer import (
    CounselorDashboardSerializer,
)  # adjust path
from utils.response_helpers import success_response
from utils.permissions import IsOwner
from django.core.cache import cache


class CounselorDashboardView(generics.GenericAPIView):
    permission_classes = [IsOwner]

    def get(self, request):
        counselor = request.user
        today = timezone.now().date()

        base_key = f"counselor_dashboard:{counselor.id}"
        cached_data = cache.get(base_key)

        if cached_data is not None:
            return success_response(data=cached_data, status_code=200)

        # Active assignments with everything nested and optimized
        assignments = (
            StudentCounselor.objects.filter(counselor=counselor, is_active=True)
            .select_related(
                "student", "student__student_profile"
            )  # pulls user + profile in one go
            .prefetch_related(
                Prefetch(
                    "counseling_sessions",
                    queryset=CounselingSession.objects.order_by("-scheduled_at"),
                )
            )
        )

        # Dashboard-level summary (optional but useful)
        total_students = assignments.count()
        todays_sessions = CounselingSession.objects.filter(
            student_counselor__counselor=counselor,
            student_counselor__is_active=True,
            scheduled_at__date=today,
            status="scheduled",
        ).count()

        serializer = CounselorDashboardSerializer(assignments, many=True)
        data = {
            "summary": {
                "total_active_students": total_students,
                "todays_upcoming_sessions": todays_sessions,
            },
            "assignments": serializer.data,
        }
        cache.set(base_key, data, 300)
        return success_response(
            data=data,
            status_code=200,
        )
