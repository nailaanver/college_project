from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('students/', views.student_list, name='student-list'),
    path('students/add/', views.add_student, name='add-student'),
    path('students/edit/<int:pk>/', views.edit_student, name='edit-student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete-student'),
    
    
    path('list/', views.teacher_list, name='teacher-list'),
    path('add/', views.add_teacher, name='add-teacher'),
    path('edit/<int:id>/', views.edit_teacher, name='edit-teacher'), 
    path('teachers/delete/<int:id>/', views.delete_teacher, name='delete-teacher'),
    
    path('parents/', views.parent_list, name='parent-list'),
    
    path('add-subject/', views.add_subject, name='add-subject'),
    path('subjects/', views.subject_list, name='subject-list'),
    





]
