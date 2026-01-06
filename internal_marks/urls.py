from django.urls import path
from . import views

urlpatterns = [
    path(
        'teacher/internal-marks/',
        views.teacher_internal_subjects,
        name='teacher-internal-subjects'
    ),
]
