from django.contrib import admin

# Register your models here.
from .models import Course, CourseBatch, CourseCategory
admin.site.register([Course, CourseBatch, CourseCategory])