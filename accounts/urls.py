from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.role_login, name='role_login'),
    path('login/student/', views.student_login, name='student-login'),
    path('login/teacher/', views.teacher_login, name='teacher-login'),
    path('login/parent/', views.parent_login, name='parent-login'),
    path('login/admin/', views.admin_login, name='admin-login'),
    path('login/admin/', views.admin_login, name='admin-login'),

]
