# dashboard/serializers/admin_dashboard_serializer.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

from course.models import CourseBatch
from course.serializers.course_serializer import GetMiniCourseSerializer

User = get_user_model()


class AdminStudentMiniSerializer(serializers.ModelSerializer):
    """Lightweight — no profile lookups, avoids N+1."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'role']


class AdminBatchDetailSerializer(serializers.ModelSerializer):
    """
    Matches your requested shape:
    batchid, students_enrolled, syllabus, course_detail
    """
    batchid = serializers.IntegerField(source='id', read_only=True)
    students_enrolled = serializers.SerializerMethodField()
    course_detail = serializers.SerializerMethodField()
    mentor_name = serializers.CharField(source='mentor.full_name', read_only=True)
    enrollment_count = serializers.IntegerField(source='current_enrollments', read_only=True)

    class Meta:
        model = CourseBatch
        fields = [
            'batchid',
            'batch_code',
            'students_enrolled',
            'enrollment_count',
            'course_detail',
            'mentor_name',
            'status',
            'schedule',
        ]

    def get_students_enrolled(self, obj):
        # View prefetches enrollments + student
        students = [e.student for e in obj.enrollments.all()]
        return AdminStudentMiniSerializer(students, many=True).data

    def get_course_detail(self, obj):
        if hasattr(obj, 'course') and obj.course:
            return GetMiniCourseSerializer(obj.course).data
        return None


class AdminDashboardSerializer(serializers.Serializer):
    """
    Plain serializer — the view builds the data dict via aggregates.
    """
    overview = serializers.DictField()
    enrollment_stats = serializers.DictField()
    assessment_stats = serializers.DictField()
    counseling_stats = serializers.DictField()
    batches = AdminBatchDetailSerializer(many=True)
    recent_student_assessments = serializers.ListField()
    recent_counseling_sessions = serializers.ListField()
