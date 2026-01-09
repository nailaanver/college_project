from django.urls import path
from . import views

urlpatterns = [
    path('send-otp/', views.parent_send_otp, name='parent_send_otp'),
    path('verify-otp/', views.parent_verify_otp, name='parent_verify_otp'),
    path('dashboard/', views.parent_dashboard, name='parent_dashboard'),  # ✅
    path('logout/', views.parent_logout, name='parent_logout'),

    path("today-attendance/", views.parent_today_attendance, name="parent_today_attendance"),
    path("parent/attendance/", views.parent_attendance_report, name="parent_attendance_report"),
    
    path('internal-marks/', views.parent_internal_marks, name='parent_internal_marks'),
    


]



