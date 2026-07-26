# # assessment/views/student_skill_result_view.py
# from rest_framework import generics, mixins, permissions
# from assessment.models import StudentSkillResult
# from assessment.serializers.student_skill_result_serializer import StudentSkillResultSerializer


# class StudentSkillResultListView(mixins.ListModelMixin, generics.GenericAPIView):
#     """
#     GET /api/skill-results/
    
#     Returns skill results. Students see their own. 
#     Counselors see assigned students. Admins see all.
#     """
#     serializer_class = StudentSkillResultSerializer
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     queryset=StudentSkillResult.objects.filter(
#                 student_assessment__status='completed'
#             ).select_related('skill', 'student_assessment')

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# assessment/views/student_skill_result_view.py
from rest_framework import generics, mixins, permissions
from assessment.models import StudentAssessment
from assessment.serializers.student_skill_result_serializer import AssessmentSkillResultSerializer


class StudentSkillResultListView(generics.ListAPIView):
    """
    GET /api/student-skill-results/
    
    Returns assessment attempts with all skill scores grouped inside.
    Each item = one assessment attempt + list of skills scored.
    """
    serializer_class = AssessmentSkillResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return StudentAssessment.objects.filter(
                student=user,
                status='completed'
            ).prefetch_related('skill_results', 'skill_results__skill').order_by('-completed_at')