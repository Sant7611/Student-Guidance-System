from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from counselling.models import CounselingSession
from counselling.serializers.CounsellingSessionSerializer import CounselingSessionReadSerializer, CounselingSessionWriteSerializer


class CounselingSessionViewSet(viewsets.ModelViewSet):
    queryset = CounselingSession.objects.all().select_related('student_counselor')
    permission_classes = [IsAuthenticated]
    ordering=['-created_at']

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return CounselingSessionReadSerializer
        return CounselingSessionWriteSerializer