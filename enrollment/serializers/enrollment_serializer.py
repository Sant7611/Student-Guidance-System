from rest_framework import serializers
from enrollment.models import Enrollment
from course.models import CourseBatch
from authentication.models import User
from django.db import transaction
from django.core.cache import cache


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))
    batch = serializers.PrimaryKeyRelatedField(queryset=CourseBatch.objects.all())
    
    class Meta:
        model = Enrollment
        fields = ['student', 'batch', 'payment_status']
        
        
    def validate(self, attrs):
        student = attrs.get('student')
        batch = attrs.get('batch')
        
        if Enrollment.objects.filter(student=student, batch=batch, is_deleted=False).exists():
            raise serializers.ValidationError("This student is already enrolled in the selected batch.")
        
        return attrs
    
    def validate_batch(self, batch):
        if batch.current_enrollments >= batch.max_seats:
            raise serializers.ValidationError("This batch has reached its maximum capacity.")
        
        return batch
    
    def validate_student(self, student):
        if student.role != 'student':
            raise serializers.ValidationError("The selected user is not a student.")
        return student
    

    
    @transaction.atomic
    def create(self, validated_data):
        batch = validated_data.pop('batch')
        batch = CourseBatch.objects.select_for_update().get(id=batch.id)
        if batch.current_enrollments >= batch.max_seats:
            raise serializers.ValidationError("This batch has reached its maximum capacity.")
        enrollment = Enrollment.objects.create(batch=batch, **validated_data)
        batch.current_enrollments += 1
        batch.save(update_fields=['current_enrollments'])
        return enrollment
    

class EnrollmentDetailSerializer(serializers.ModelSerializer):
    student_details = serializers.SerializerMethodField()
    batch_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student_details', 'batch_detail',
            'enrolled_at', 'payment_status',
            'created_at', 'updated_at'
        ]
        
    def get_student_details(self, obj):
        return { "id": obj.student.id, "username": obj.student.username, "email": obj.student.email }
    
    def get_batch_detail(self, obj):
        return { "id": obj.batch.id, "batch_code": obj.batch.batch_code, "course": obj.batch.course.title, "mentor":obj.batch.mentor.username }