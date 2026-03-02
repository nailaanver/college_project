from django.shortcuts import render, redirect
from students.models import Student
from teachers.models import Subject, Teacher
from dashboard.models import TimeTable
from django.contrib import messages



def home(request):
    return render(request, 'home.html')


def add_timetable(request):
    subjects = Subject.objects.all()

    courses = Student.COURSE_CHOICES
    semesters = Student.SEMESTER_CHOICES
    days = TimeTable.DAYS_OF_WEEK

    teachers = Teacher.objects.all()

    if request.method == 'POST':
        course = request.POST.get('course')
        semester = request.POST.get('semester')
        day = request.POST.get('day')
        period_number = request.POST.get('period_number')
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')

        # ✅ 1. CHECK PERIOD DUPLICATE (already correct)
        exists = TimeTable.objects.filter(
            course=course,
            semester=semester,
            day=day,
            period_number=period_number
        ).exists()

        if exists:
            messages.error(
                request,
                "This period is already assigned for the selected course, semester and day."
            )
        else:
            # ✅ 2. CHECK TEACHER CLASH
            teacher_busy = TimeTable.objects.filter(
                teacher_id=teacher_id,
                day=day,
                period_number=period_number
            ).exists()

            if teacher_busy:
                messages.error(
                    request,
                    "This teacher is already assigned for this period."
                )
            else:
                TimeTable.objects.create(
                    course=course,
                    semester=semester,
                    day=day,
                    period_number=period_number,
                    subject_id=subject_id,
                    teacher_id=teacher_id
                )
                messages.success(request, "Timetable added successfully!")
                return redirect('add-timetable')

        # ✅ FILTER AVAILABLE TEACHERS AGAIN (IMPORTANT)
        busy_teacher_ids = TimeTable.objects.filter(
            day=day,
            period_number=period_number
        ).values_list('teacher_id', flat=True)

        teachers = Teacher.objects.exclude(id__in=busy_teacher_ids)

    return render(request, 'adminpanel/add_timetable.html', {
        'subjects': subjects,
        'teachers': teachers,   # 👈 ONLY AVAILABLE TEACHERS
        'courses': courses,
        'semesters': semesters,
        'days': days,
    })


def timetable_filter(request):
    return render(request, 'adminpanel/timetable_filter.html', {
        'courses': Student.COURSE_CHOICES,
        'semesters': Student.SEMESTER_CHOICES,
    })


def timetable_view(request):
    course = request.GET.get('course')
    semester = request.GET.get('semester')

    timetables = TimeTable.objects.filter(
        course=course,
        semester=semester
    ).select_related(
        'subject', 'teacher'
    )

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = range(1, 8)  # ✅ 7 periods only

    return render(request, 'adminpanel/timetable_view.html', {
        'timetables': timetables,
        'course': course,
        'semester': semester,
        'days': days,
        'periods': periods,
    })

# def splash(request):
#     if request.session.get('splash_shown'):
#         return redirect('/home/')   # skip splash if already shown

#     request.session['splash_shown'] = True
#     return render(request, 'splash.html')

# from django.shortcuts import redirect, render

# def home_entry(request):
#     if not request.session.get('home_opened'):
#         request.session['home_opened'] = True
#         return redirect('/splash/')
    
#     return render(request, 'dashboard/home.html')