from django.urls import path
from .views import student_dashboard_view, mentor_dashboard_view, counselor_dashboard_view

urlpatterns=[
    path('dashboard/student/', student_dashboard_view.StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/mentor/', mentor_dashboard_view.MentorDashboardView.as_view(), name='mentor_dashboard'),
    path('dashboard/counselor/', counselor_dashboard_view.CounselorDashboardView.as_view(), name='counselor_dashboard')
]