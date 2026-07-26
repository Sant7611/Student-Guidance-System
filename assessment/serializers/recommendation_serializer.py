from rest_framework import serializers


class GapSkillSerializer(serializers.Serializer):
    skill_id = serializers.IntegerField()
    skill_name = serializers.CharField()
    required_score = serializers.IntegerField()
    student_score = serializers.IntegerField()
    gap = serializers.IntegerField()
    weightage = serializers.FloatField()


class LearningPathSerializer(serializers.Serializer):
    sequence = serializers.IntegerField()
    course_id = serializers.IntegerField()
    course_title = serializers.CharField()


class RecommendationSerializer(serializers.Serializer):
    career_id = serializers.IntegerField()
    career_title = serializers.CharField()
    industry = serializers.CharField()
    match_score = serializers.IntegerField()
    is_ready = serializers.BooleanField()
    total_skills = serializers.IntegerField()
    met_skills = serializers.IntegerField()
    gap_skills = GapSkillSerializer(many=True)
    learning_path = LearningPathSerializer(many=True)