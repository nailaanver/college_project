from django.urls import path
from . import views

urlpatterns = [
    # TEACHER
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

    # ADMIN
    path(
        'adminpanel/internal-marks/',
        views.admin_internal_subjects,
        name='admin-internal-subjects'
    ),
    path(
        'adminpanel/internal-marks/<str:course>/<int:semester>/<int:subject_id>/',
        views.admin_review_marks,
        name='admin-review-marks'
    ),
]
