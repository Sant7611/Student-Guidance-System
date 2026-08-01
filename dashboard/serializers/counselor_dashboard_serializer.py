from rest_framework import serializers
from django.utils import timezone
from counselling.models import StudentCounselor, CounselingSession
from counselling.serializers.CounsellingSessionSerializer import CounselingSessionReadSerializer
from authentication.serializers.student_register_serializer import StudentUserMiniSerializer  # adjust import path


class CounselorDashboardSerializer(serializers.ModelSerializer):
    """
    Maps to your requested shape:
      - id              -> assignment id (like batchid)
      - student         -> enrolled student detail
      - recent_sessions -> session history (like syllabus)
      - next_session    -> nearest upcoming session
      - session_stats   -> meta counts (like course_detail)
    """
    student = StudentUserMiniSerializer(read_only=True)
    recent_sessions = serializers.SerializerMethodField()
    next_session = serializers.SerializerMethodField()
    session_stats = serializers.SerializerMethodField()

    class Meta:
        model = StudentCounselor
        fields = [
            'id',
            'student',
            'assigned_at',
            'is_active',
            'recent_sessions',
            'next_session',
            'session_stats',
        ]

    def get_recent_sessions(self, obj): 
        # View prefetches these ordered by -scheduled_at
        sessions = list(obj.counseling_sessions.all())[:5]
        return CounselingSessionReadSerializer(sessions, many=True).data

    def get_next_session(self, obj):
        now = timezone.now()
        upcoming = None
        for session in obj.counseling_sessions.all():
            if session.status == 'scheduled' and session.scheduled_at >= now:
                if upcoming is None or session.scheduled_at < upcoming.scheduled_at:
                    upcoming = session
        return CounselingSessionReadSerializer(upcoming).data if upcoming else None

    def get_session_stats(self, obj):
        # Uses the prefetched cache; no extra queries
        sessions = list(obj.counseling_sessions.all())
        stats = {'total': len(sessions), 'scheduled': 0, 'completed': 0, 'cancelled': 0, 'no_show': 0}
        for s in sessions:
            if s.status in stats:
                stats[s.status] += 1
        return stats