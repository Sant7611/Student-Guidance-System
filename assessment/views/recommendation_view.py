from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from yaml import serializer
from ..recommendation import CareerRecommendationEngine
from ..serializers.recommendation_serializer import RecommendationSerializer
from utils.response_helpers import success_response, error_response

class RecommendationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        student = request.user
        if not student:
            return error_response(
                message="Student profile not found.",
                status_code=404
            )

        engine = CareerRecommendationEngine(student)
        raw_data = engine.get_recommendations(min_match=30, top_n=5)

        serializer = RecommendationSerializer(data=raw_data, many=True)
        if not serializer.is_valid():
            return error_response(message=serializer.errors, status_code=400)

        return success_response(data=serializer.data, status_code=200)