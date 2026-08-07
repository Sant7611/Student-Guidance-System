from rest_framework import serializers
from course.serializers.course_serializer import GetMiniCourseSerializer
from course.serializers.course_batch_serializer import BatchStudentSerializer
from course.models import CourseBatch
from django.contrib.auth import get_user_model
User= get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MentorBatchSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField(read_only=True)
    enrolled_students = serializers.SerializerMethodField(read_only=True)
    course = GetMiniCourseSerializer(read_only=True)
    class Meta:
        model = CourseBatch
        fields=['id', 'batch_code', 'students', 'enrolled_students', 'status', 'start_date', 'end_date',
                'current_enrollments', 'max_seats', 'schedule', 'course']
    
    
    def get_students(self, batch):
        enrollments = batch.enrollments.all()
        students = [enrollment.student for enrollment in enrollments]
        return StudentSerializer(students, many=True).data

    def get_enrolled_students(self, batch):
        return BatchStudentSerializer(
            [enrollment.student for enrollment in batch.enrollments.all()],
            many=True,
        ).data
