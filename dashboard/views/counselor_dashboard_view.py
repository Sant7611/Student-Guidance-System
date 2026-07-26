from rest_framework.views import APIView
from django.db.models import Prefetch
from django.utils import timezone
from counselling.models import StudentCounselor, CounselingSession
from dashboard.serializers.counselor_dashboard_serializer import CounselorDashboardSerializer  # adjust path
from utils.response_helpers import success_response
from rest_framework.permissions import IsAuthenticated


class CounselorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        counselor = request.user
        today = timezone.now().date()

        # Active assignments with everything nested and optimized
        assignments = (
            StudentCounselor.objects
            .filter(counselor=counselor, is_active=True)
            .select_related('student', 'student__student_profile')  # pulls user + profile in one go
            .prefetch_related(
                Prefetch(
                    'counseling_sessions',
                    queryset=CounselingSession.objects.order_by('-scheduled_at')
                )
            )
        )

        # Dashboard-level summary (optional but useful)
        total_students = assignments.count()
        todays_sessions = CounselingSession.objects.filter(
            student_counselor__counselor=counselor,
            student_counselor__is_active=True,
            scheduled_at__date=today,
            status='scheduled'
        ).count()

        serializer = CounselorDashboardSerializer(assignments, many=True)

        return success_response(data={
            'summary': {
                'total_active_students': total_students,
                'todays_upcoming_sessions': todays_sessions,
            },
            'assignments': serializer.data,
        }, status_code=200)