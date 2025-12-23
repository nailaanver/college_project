from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('students/', views.student_list, name='student-list'),
    path('students/add/', views.add_student, name='add-student'),
    path('students/edit/<int:pk>/', views.edit_student, name='edit-student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete-student'),

]
