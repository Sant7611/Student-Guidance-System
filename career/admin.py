from django.contrib import admin

# Register your models here.
from .models import Career, CareerSkill, CareerPath
admin.site.register([Career, CareerSkill, CareerPath])