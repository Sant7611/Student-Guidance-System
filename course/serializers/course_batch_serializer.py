from rest_framework import serializers
from course.models import Course, CourseBatch
from course.serializers.course_serializer import GetMiniCourseSerializer
from authentication.models import User


class BatchStudentSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'role']


def get_enrolled_students(batch):
    return BatchStudentSerializer(
        [enrollment.student for enrollment in batch.enrollments.all()],
        many=True,
    ).data

class CourseBatchSerializer(serializers.ModelSerializer):
    course_details = serializers.SerializerMethodField()
    enrolled_students = serializers.SerializerMethodField()
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)
    class Meta:
        model = CourseBatch
        fields = "__all__"
        
    def get_course_details(self, obj):
        return GetMiniCourseSerializer(obj.course).data

    def get_enrolled_students(self, obj):
        return get_enrolled_students(obj)
    

class GetMiniCourseBatchSerializer(serializers.ModelSerializer):
    course = GetMiniCourseSerializer(read_only=True)
    mentor = serializers.CharField(source='mentor.username', read_only=True)
    enrolled_students = serializers.SerializerMethodField()
    class Meta:
        model = CourseBatch
        fields = [
            'id', 'batch_code', 'status', 'start_date', 'end_date',
            'max_seats', 'current_enrollments', 'schedule', 'mentor',
            'course', 'enrolled_students',
        ]

    def get_enrolled_students(self, obj):
        return get_enrolled_students(obj)
