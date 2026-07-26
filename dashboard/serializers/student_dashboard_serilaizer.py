from rest_framework import serializers
from assessment.serializers.student_assessment_serializer import StudentUserMiniSerializer
from course.serializers.course_batch_serializer import GetMiniCourseBatchSerializer
from enrollment.models import Enrollment
from counselling.models import CounselingSession
from assessment.models import StudentAssessment

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    batch = GetMiniCourseBatchSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'batch', 'status', 'payment_status', 'enrolled_at']
        

class StudentCounselingSessionSerializer(serializers.ModelSerializer):
    counselor = serializers.CharField(source='counselor.username', read_only=True)
    
    class Meta:
        model = CounselingSession
        fields = ['id', 'counselor', 'scheduled_at', 'status', 'notes']

class StudentAssessmentSerializer(serializers.ModelSerializer):
    """
    Read-only. Shows all results including computed properties.
    """
    
    class Meta:
        model = StudentAssessment
        fields = [
            'id', 'score', 
            'has_passed', 'weak_skills',  
            'attempt_number', 'status', 
            'time_taken_seconds', 'completed_at'
        ]