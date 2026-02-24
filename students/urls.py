from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student-dashboard'),
    path('profile/', views.student_profile, name='student-profile'),
    path('attendance/', views.student_attendance, name='student-attendance'),
    path('marks/', views.student_internal_marks, name='student-marks'),
    path('timetable/', views.student_timetable, name='student-timetable'),
    path('logout/', views.student_logout, name='student-logout'),
    
    path('history/', views.semester_history, name='semester-history'),
    path('student/payment-history/', views.student_payment_history, name='student-payment-history'),

]
