from rest_framework import viewsets
from course.models import Course
from course.serializers.course_serializer import PostCourseSerializer, GetCourseSerializer
from utils.permissions import AdminOnlyPost
from django.core.cache import cache
class CourseView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [AdminOnlyPost]
    ordering=['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetCourseSerializer
        return PostCourseSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        cache.delete(f"admin_dashboard:{self.request.user.id}")