from rest_framework.views import APIView
from utils.response_helpers import success_response, error_response
from counselling.models import StudentCounselor, CounselingSession
from assessment.models import StudentAssessment
from enrollment.models import Enrollment
from dashboard.serializers.student_dashboard_serilaizer import StudentEnrollmentSerializer, StudentAssessmentSerializer, StudentCounselingSessionSerializer

class StudentDashboardView(APIView):
    
    def get(self, request):
        if request.user.role != 'student':
            return error_response(message="Unauthorized access", status_code=403)
        
        student = request.user
        
        counselling = CounselingSession.objects.filter(student_counselor__student=student).order_by('-created_at').select_related('student_counselor__counselor', 'student_counselor')

        enrolled_courses = Enrollment.objects.filter(student=student, is_deleted=False).select_related('batch')
        
        assessments = StudentAssessment.objects.filter(student=student).order_by('-created_at')
        
        return success_response(data = {
            "counselling": StudentCounselingSessionSerializer(counselling, many=True).data,
            "enrolled_courses": StudentEnrollmentSerializer(enrolled_courses, many=True).data,
            "assessments": StudentAssessmentSerializer(assessments, many=True).data
        },status_code=200) 