from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher-dashboard'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('timetable/', views.teacher_timetable, name='teacher_timetable'),
   


]
