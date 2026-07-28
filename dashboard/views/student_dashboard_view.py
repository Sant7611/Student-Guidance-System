from rest_framework import generics
from utils.response_helpers import success_response, error_response
from counselling.models import CounselingSession
from assessment.models import StudentAssessment
from enrollment.models import Enrollment
from dashboard.serializers.student_dashboard_serilaizer import (
    StudentEnrollmentSerializer,
    StudentAssessmentSerializer,
    StudentCounselingSessionSerializer,
)
from utils.permissions import IsOwner
from django.core.cache import cache


class StudentDashboardView(generics.GenericAPIView):
    permission_classes = [IsOwner]

    def get(self, request):
        if request.user.role != "student":
            return error_response(message="Unauthorized access", status_code=403)

        cache_key = f"student_dashboard:{request.user.id}"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return success_response(data=cached_data, status_code=200)

        student = request.user

        counselling = (
            CounselingSession.objects.filter(student_counselor__student=student)
            .order_by("-created_at")
            .select_related("student_counselor__counselor", "student_counselor")
        )
        counselling_data = StudentCounselingSessionSerializer(
            counselling, many=True
        ).data

        enrolled_courses = Enrollment.objects.filter(
            student=student, is_deleted=False
        ).select_related("batch")
        enrolled_courses_data = StudentEnrollmentSerializer(
            enrolled_courses, many=True
        ).data

        assessments = StudentAssessment.objects.filter(student=student).order_by(
            "-created_at"
        )
        assessments_data = StudentAssessmentSerializer(assessments, many=True).data

        data = {
            "counselling": counselling_data,
            "enrolled_courses": enrolled_courses_data,
            "assessments": assessments_data,
        }

        cache.set(cache_key, data, 300)

        return success_response(data=data, status_code=200)
