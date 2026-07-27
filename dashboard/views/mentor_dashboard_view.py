from rest_framework import generics
from utils.response_helpers import success_response, error_response
from course.models import CourseBatch
from enrollment.models import Enrollment
from dashboard.serializers.mentor_dashboard_serilaizer import MentorBatchSerializer
from django.db.models import Prefetch
from utils.permissions import IsOwner



class MentorDashboardView(generics.GenericAPIView):
    permission_classes = [IsOwner]

    def get(self, request):
        if request.user.role != 'mentor':
            return error_response(message="Unauthorized access", status_code=403)
        
        mentor = request.user

        batches = CourseBatch.objects.filter(mentor=mentor).select_related('course').prefetch_related(Prefetch('enrollments', queryset=Enrollment.objects.select_related('student')
        )
    )
        batches = MentorBatchSerializer(batches, many=True)

        return success_response(data = {
            
            'batches': batches.data
            },status_code=200) 