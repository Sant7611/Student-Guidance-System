from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from counselling.models import StudentCounselor, CounselingSession
from enrollment.models import Enrollment
from assessment.models import StudentAssessment
from course.models import CourseBatch


@receiver([post_save, post_delete], sender=StudentCounselor)
def clear_counseling_cache(sender, instance, **kwargs):
    cache.delete(f"counselor_dashboard:{instance.counselor_id}")
    cache.delete("admin_dashboard:counseling_stats")
    cache.delete("admin_dashboard:recent_counseling_sessions")


@receiver([post_save, post_delete], sender=Enrollment)
def clear_enrollment_cache(sender, instance, **kwargs):
    cache.delete(f"mentor_dashboard:{instance.batch.mentor_id}")
    cache.delete(f"student_dashboard:{instance.student_id}")
    cache.delete("admin_dashboard:enrollment_stats")


@receiver([post_save, post_delete], sender=StudentAssessment)
def clear_assessment_cache(sender, instance, **kwargs):
    cache.delete(f"student_dashboard:{instance.student_id}")
    cache.delete("admin_dashboard:assessment_stats")
    cache.delete("admin_dashboard:recent_student_assessment")


@receiver([post_save, post_delete], sender=CourseBatch)
def clear_batch_cache(sender, instance, **kwargs):
    cache.delete(f"mentor_dashboard:{instance.mentor_id}")


@receiver([post_save, post_delete], sender=CounselingSession)
def clear_counseling_session_cache(sender, instance, **kwargs):
    cache.delete("admin_dashboard:recent_counseling_sessions")
    cache.delete("admin_dashboard:counseling_stats")  # Added
    cache.delete(f"counselor_dashboard:{instance.student_counselor.counselor_id}")
    cache.delete(f"student_dashboard:{instance.student_counselor.student_id}") 