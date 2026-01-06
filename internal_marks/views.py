from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import TimeTable

@login_required
def teacher_internal_subjects(request):
    teacher = request.user.teacher  # assuming OneToOne with User

    timetables = (
        TimeTable.objects
        .filter(teacher=teacher)
        .select_related('subject')
        .values(
            'course',
            'semester',
            'subject__id',
            'subject__name'
        )
        .distinct()
    )

    context = {
        'subjects': timetables
    }
    return render(
        request,
        'internal_marks/teacher_subject_list.html',
        context
    )
