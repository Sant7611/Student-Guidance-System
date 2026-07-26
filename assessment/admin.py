from django.contrib import admin

# Register your models here.
from .models import Assessment, AssessmentSkill, StudentAssessment, StudentSkillResult

admin.site.register([Assessment, AssessmentSkill, StudentAssessment, StudentSkillResult])
    