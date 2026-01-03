from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_home, name='attendance_home'),
    path('mark/<int:timetable_id>/', views.mark_attendance, name='mark_attendance'),
    path('summary/<int:timetable_id>/', views.attendance_summary, name='attendance_summary'),
    path('edit/<int:timetable_id>/', views.edit_attendance, name='edit_attendance'),

]
