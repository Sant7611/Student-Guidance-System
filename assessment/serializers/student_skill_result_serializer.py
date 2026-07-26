# # assessment/serializers/student_skill_result_serializer.py
# from rest_framework import serializers
# from assessment.models import StudentSkillResult
# from skill.serializers.skill_serializer import SkillMiniReadSerializer

# class StudentSkillResultMiniSerializer(serializers.ModelSerializer):
#     skill = SkillMiniReadSerializer(read_only=True)
#     class Meta:
#         model=StudentSkillResult
#         fields=['skill', 'score']


# class StudentSkillResultSerializer(serializers.ModelSerializer):
#     """
#     Read-only serializer for student skill results.
#     Includes nested skill details for easy frontend consumption.
#     """
#     skill_results = StudentSkillResultMiniSerializer(read_only=True, many=True)
#     assessment_title = serializers.CharField(
#         source='student_assessment.assessment.title',
#         read_only=True
#     )
#     student = serializers.CharField(source='student_assessment.student.get_full_name', read_only=True)
#     assessment_id = serializers.IntegerField(
#         source='student_assessment.assessment.id',
#         read_only=True
#     )

#     class Meta:
#         model = StudentSkillResult
#         fields = [
#             'id',
#             'student',
#             'assessment_id',
#             'assessment_title',
#             'skill_results',
#             'score',
#             'created_at',
#             'updated_at'
#         ]
#         read_only_fields = fields


# assessment/serializers/student_skill_result_serializer.py
from rest_framework import serializers
from assessment.models import StudentSkillResult, StudentAssessment
from skill.serializers.skill_serializer import SkillMiniReadSerializer


class SkillResultMiniSerializer(serializers.ModelSerializer):
    """Single skill score — nested inside assessment result."""
    skill = SkillMiniReadSerializer(read_only=True)

    class Meta:
        model = StudentSkillResult
        fields = ['skill', 'score']


class AssessmentSkillResultSerializer(serializers.ModelSerializer):
    """
    Assessment-level result with all skills grouped inside.
    One object per assessment attempt.
    """
    assessment_id = serializers.IntegerField(source='assessment.id', read_only=True)
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    overall_score = serializers.IntegerField(source='score', read_only=True)
    status = serializers.CharField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)
    skill_results = SkillResultMiniSerializer(many=True, read_only=True)

    class Meta:
        model = StudentAssessment
        fields = [
            'id',
            'assessment_id',
            'assessment_title',
            'overall_score',
            'status',
            'completed_at',
            'skill_results',
        ]