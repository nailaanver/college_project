from django.urls import path
from . import views

urlpatterns = [
    path('send-otp/', views.parent_send_otp, name='parent_send_otp'),
    path('verify-otp/', views.parent_verify_otp, name='parent_verify_otp'),
    path('dashboard/', views.parent_dashboard, name='parent_dashboard'),  # ✅
    path('logout/', views.parent_logout, name='parent_logout'),


]
