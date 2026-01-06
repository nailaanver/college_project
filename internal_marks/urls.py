from django.urls import path
from . import views

urlpatterns = [
    path(
        'teacher/internal-marks/',
        views.teacher_internal_subjects,
        name='teacher-internal-subjects'
    ),
    path(
        'teacher/internal-marks/<str:course>/<int:semester>/<int:subject_id>/',
        views.teacher_enter_marks,
        name='teacher-enter-marks'
    ),
]
