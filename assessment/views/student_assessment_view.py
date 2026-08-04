from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from assessment.models import (
    StudentAssessment,
    AssessmentSkill,
    StudentSkillResult,
)

from assessment.serializers.student_assessment_serializer import (
    StudentAssessmentReadSerializer,
    StudentAssessmentCreateSerializer,
    StudentAssessmentSubmitSerializer,
)

from notifications.services import NotificationService
from utils.response_helpers import success_response, error_response


class StudentAssessmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing student assessment attempts.
    """

    permission_classes = [IsAuthenticated]

    queryset = StudentAssessment.objects.all()
    ordering = ["-created_at"]

    def get_serializer_class(self):

        if self.action == "start":
            return StudentAssessmentCreateSerializer

        elif self.action == "submit":
            return StudentAssessmentSubmitSerializer

        return StudentAssessmentReadSerializer

    def get_queryset(self):

        user = self.request.user

        if hasattr(user, "role") and user.role == "student":
            return self.queryset.filter(student=user)

        return self.queryset

    # ==========================================================
    # START ASSESSMENT
    # ==========================================================

    @action(detail=False, url_path="start", methods=["post"])
    def start(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        student_assessment = serializer.save()

        NotificationService.send_notification(
            user=request.user,
            title="Assessment Started",
            body=(
                f"You have started the assessment "
                f"{student_assessment.assessment.title}."
            ),
            notification_type="assessment_started",
        )

        read_serializer = StudentAssessmentReadSerializer(student_assessment)

        return success_response(data=read_serializer.data, status_code=201)

    # ==========================================================
    # SUBMIT ASSESSMENT
    # ==========================================================

    @action(detail=True, url_path="submit", methods=["post"])
    def submit(self, request, pk=None):

        attempt = self.get_object()

        # -------------------------------
        # Validate status
        # -------------------------------

        if attempt.status != StudentAssessment.Status.IN_PROGRESS:

            return error_response(
                errors="Cannot submit. Attempt is not in progress.", status_code=400
            )

        # -------------------------------
        # Validate ownership
        # -------------------------------

        if attempt.student != request.user:

            return error_response(
                errors="You can only submit your own attempts.", status_code=403
            )

        # -------------------------------
        # Validate submitted data
        # -------------------------------

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        answers = serializer.validated_data.get("answers")

        time_taken = serializer.validated_data.get("time_taken_seconds")

        # -------------------------------
        # Calculate skill scores
        # -------------------------------

        skill_breakdown = self._calculate_skill_breakdown(attempt.assessment, answers)

        # -------------------------------
        # Calculate overall score
        # -------------------------------

        overall_score = self._calculate_overall_score(
            skill_breakdown, attempt.assessment
        )

        # -------------------------------
        # Save skill results
        # -------------------------------

        for skill_data in skill_breakdown["skill_scores"]:

            StudentSkillResult.objects.create(
                student_assessment=attempt,
                skill_id=skill_data["skill_id"],
                score=skill_data["score"],
            )

        # -------------------------------
        # Complete assessment
        # -------------------------------

        attempt.complete(score=overall_score, answers=answers, time_taken=time_taken)

        # -------------------------------
        # Notification
        # -------------------------------

        NotificationService.send_notification(
            user=attempt.student,
            title="Assessment Completed",
            body=(
                f"You have completed the assessment "
                f"{attempt.assessment.title}. "
                f"Your score is {overall_score}%."
            ),
            notification_type="assessment_completed",
        )

        read_serializer = StudentAssessmentReadSerializer(attempt)

        return success_response(data=read_serializer.data, status_code=200)

    # ==========================================================
    # ABANDON ASSESSMENT
    # ==========================================================

    @action(detail=True, url_path="abandon", methods=["post"])
    def abandon(self, request, pk=None):

        attempt = self.get_object()

        if attempt.status != StudentAssessment.Status.IN_PROGRESS:

            return error_response(
                errors="Can only abandon in-progress attempts.", status_code=400
            )

        if attempt.student != request.user:

            return error_response(
                errors="You can only abandon your own attempts.", status_code=403
            )

        attempt.abandon()

        NotificationService.send_notification(
            user=attempt.student,
            title="Assessment Abandoned",
            body=(f"You have abandoned the assessment " f"{attempt.assessment.title}."),
            notification_type="assessment_abandoned",
        )

        return success_response(
            data={"message": "Assessment abandoned", "status": attempt.status},
            status_code=200,
        )

    # ==========================================================
    # CALCULATE SKILL BREAKDOWN
    # ==========================================================

    def _calculate_skill_breakdown(self, assessment, answers):

        questions = assessment.questions

        student_answers = answers.get("answers", [])

        question_map = {q["id"]: q for q in questions}

        skill_stats = {}

        for answer in student_answers:

            question_id = answer.get("question_id")

            student_answer = answer.get("answer")

            question = question_map.get(question_id)

            if not question:
                continue

            skill_id = question.get("skill_id")

            correct_answer = question.get("correct_answer")

            if skill_id not in skill_stats:

                skill_stats[skill_id] = {"correct": 0, "total": 0}

            skill_stats[skill_id]["total"] += 1

            if student_answer == correct_answer:

                skill_stats[skill_id]["correct"] += 1

        skill_scores = []

        for skill_id, stats in skill_stats.items():

            percentage = (
                round((stats["correct"] / stats["total"]) * 100)
                if stats["total"] > 0
                else 0
            )

            skill_scores.append({"skill_id": skill_id, "score": percentage})

        return {"skill_scores": skill_scores}

    # ==========================================================
    # CALCULATE OVERALL SCORE
    # ==========================================================

    def _calculate_overall_score(self, skill_breakdown, assessment):

        skill_scores = skill_breakdown.get("skill_scores", [])

        total_score = 0

        total_weight = 0

        for skill_data in skill_scores:

            skill_id = skill_data.get("skill_id")

            score = skill_data.get("score", 0)

            try:

                assessment_skill = AssessmentSkill.objects.get(
                    assessment=assessment, skill_id=skill_id
                )

                weight = assessment_skill.weightage

            except AssessmentSkill.DoesNotExist:

                weight = 100 / len(skill_scores) if skill_scores else 0

            total_score += score * weight

            total_weight += weight

        return round(total_score / total_weight) if total_weight > 0 else 0
