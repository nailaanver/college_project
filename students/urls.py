from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student-dashboard'),
    path('logout/', views.student_logout, name='student-logout'),

]