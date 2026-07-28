# dashboard/views/admin_dashboard_view.py
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import (
    Avg,
    Case,
    Count,
    F,
    IntegerField,
    Prefetch,
    Q,
    Sum,
    Value,
    When,
)
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from assessment.models import Assessment, StudentAssessment
from counselling.models import CounselingSession, StudentCounselor
from course.models import CourseBatch
from dashboard.serializers.admin_dashboard_serializer import AdminDashboardSerializer
from enrollment.models import Enrollment
from utils.response_helpers import success_response

User = get_user_model()


class AdminDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        today = timezone.now().date()

        # ── 1. USER OVERVIEW (single query) ──
        overview = cache.get("admin_dashboard:overview")
        if overview is None:
            overview = User.objects.aggregate(
                total_students=Count(
                    "id", filter=Q(role="student", is_deleted=False)
                ),
                total_mentors=Count(
                    "id", filter=Q(role="mentor", is_deleted=False)
                ),
                total_counselors=Count(
                    "id", filter=Q(role="counselor", is_deleted=False)
                ),
                total_admins=Count(
                    "id", filter=Q(role="super_admin", is_deleted=False)
                ),
            )
            overview["total_ongoing_batches"] = CourseBatch.objects.filter(
                status="ongoing"
            ).count()
            cache.set("admin_dashboard:overview", overview, 600)

        # ── 2. ENROLLMENT STATS (single query) ──
        enrollment_stats = cache.get("admin_dashboard:enrollment_stats")
        if enrollment_stats is None:
            enrollment_stats = Enrollment.objects.aggregate(
                total=Count("id"),
                payment_pending=Count(
                    "id", filter=Q(payment_status="pending")
                ),
                payment_paid=Count("id", filter=Q(payment_status="paid")),
                payment_partial=Count(
                    "id", filter=Q(payment_status="partial")
                ),
            )
            cache.set(
                "admin_dashboard:enrollment_stats", enrollment_stats, 600
            )

        # ── 3. ASSESSMENT STATS ──
        assessment_stats = cache.get("admin_dashboard:assessment_stats")
        if assessment_stats is None:
            completed_attempts = StudentAssessment.objects.filter(
                status="completed"
            )

            agg = completed_attempts.aggregate(
                avg_score=Avg("score"),
                total_completed=Count("id"),
                total_passed=Sum(
                    Case(
                        When(
                            score__gte=F("assessment__passing_score"),
                            then=Value(1),
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                ),
            )

            by_type = {}
            for atype, label in Assessment.AssessmentType.choices:
                by_type[label] = StudentAssessment.objects.filter(
                    assessment__assessment_type=atype
                ).count()

            assessment_stats = {
                "total_active_assessments": Assessment.objects.filter(
                    is_active=True
                ).count(),
                "total_attempts": StudentAssessment.objects.count(),
                "completed_attempts": agg["total_completed"] or 0,
                "avg_score": (
                    round(agg["avg_score"], 2)
                    if agg["avg_score"]
                    else 0
                ),
                "pass_rate": (
                    round(
                        (agg["total_passed"] or 0)
                        / agg["total_completed"]
                        * 100,
                        2,
                    )
                    if agg["total_completed"]
                    else 0
                ),
                "by_type": by_type,
            }
            cache.set(
                "admin_dashboard:assessment_stats", assessment_stats, 600
            )

        # ── 4. COUNSELING STATS ──
        counseling_stats = cache.get("admin_dashboard:counseling_stats")
        if counseling_stats is None:
            active_assignments = StudentCounselor.objects.filter(
                is_active=True
            ).count()

            assigned_ids = StudentCounselor.objects.filter(
                is_active=True
            ).values_list("student_id", flat=True)

            unassigned_students = (
                User.objects.filter(role="student")
                .exclude(id__in=assigned_ids)
                .count()
            )

            counseling_stats = CounselingSession.objects.aggregate(
                total_sessions=Count("id"),
                scheduled=Count("id", filter=Q(status="scheduled")),
                completed=Count("id", filter=Q(status="completed")),
                cancelled=Count("id", filter=Q(status="cancelled")),
                no_show=Count("id", filter=Q(status="no_show")),
                today_scheduled=Count(
                    "id",
                    filter=Q(status="scheduled", scheduled_at__date=today),
                ),
            )
            counseling_stats["active_assignments"] = active_assignments
            counseling_stats["unassigned_students"] = unassigned_students
            cache.set(
                "admin_dashboard:counseling_stats", counseling_stats, 600
            )

        # ── 5. BATCHES ──
        batches = (
            CourseBatch.objects.select_related("course", "mentor")
            .prefetch_related(
                Prefetch(
                    "enrollments",
                    queryset=Enrollment.objects.select_related("student"),
                )
            )
            .order_by("-created_at")[:8]
        )

        # ── 6. RECENT ACTIVITY ──
        recent_student_assessments = cache.get(
            "admin_dashboard:recent_student_assessment"
        )
        if recent_student_assessments is None:
            recent_assessments = (
                StudentAssessment.objects.select_related(
                    "student", "assessment"
                )
                .order_by("-created_at")[:5]
            )

            recent_student_assessments = [
                {
                    "id": a.id,
                    "student": a.student.username,
                    "assessment": a.assessment.title,
                    "score": a.score,
                    "status": a.status,
                    "attempt_number": a.attempt_number,
                    "created_at": a.created_at,
                }
                for a in recent_assessments
            ]
            cache.set(
                "admin_dashboard:recent_student_assessment",
                recent_student_assessments,
                60,
            )

        recent_counseling_sessions = cache.get(
            "admin_dashboard:recent_counseling_sessions"
        )
        if recent_counseling_sessions is None:
            recent_sessions = (
                CounselingSession.objects.select_related(
                    "student_counselor__student",
                    "student_counselor__counselor",
                )
                .order_by("-scheduled_at")[:4]
            )
            recent_counseling_sessions = [
                {
                    "id": s.id,
                    "student": s.student_counselor.student.username,
                    "counselor": s.student_counselor.counselor.username,
                    "scheduled_at": s.scheduled_at,
                    "status": s.status,
                }
                for s in recent_sessions
            ]
            cache.set(
                "admin_dashboard:recent_counseling_sessions",
                recent_counseling_sessions,
                60,
            )

        # ── 7. PACKAGE & RESPOND ──
        data = {
            "overview": overview,
            "enrollment_stats": enrollment_stats,
            "assessment_stats": assessment_stats,
            "counseling_stats": counseling_stats,
            "batches": batches,
            "recent_student_assessments": recent_student_assessments,
            "recent_counseling_sessions": recent_counseling_sessions,
        }

        serializer = AdminDashboardSerializer(data)
        return success_response(data=serializer.data, status_code=200)