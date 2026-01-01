from django.shortcuts import render, redirect
from students.models import Student
from teachers.models import Subject, Teacher
from dashboard.models import TimeTable
from django.contrib import messages



def home(request):
    return render(request, 'home.html')


def add_timetable(request):
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()

    courses = Student.COURSE_CHOICES
    semesters = Student.SEMESTER_CHOICES
    days = TimeTable.DAYS_OF_WEEK

    if request.method == 'POST':
        course = request.POST.get('course')
        semester = request.POST.get('semester')
        day = request.POST.get('day')
        period_number = request.POST.get('period_number')
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')

        # ✅ CHECK DUPLICATE
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
            TimeTable.objects.create(
                course=course,
                semester=semester,
                day=day,
                period_number=period_number,
                subject_id=subject_id,
                teacher_id=teacher_id
            )
            messages.success(request, "Timetable added successfully!")
            return redirect('add-timetable')  # stay on same page

    return render(request, 'adminpanel/add_timetable.html', {
        'subjects': subjects,
        'teachers': teachers,
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
    ).select_related('subject', 'teacher').order_by('day', 'period_number')

    return render(request, 'adminpanel/timetable_view.html', {
        'timetables': timetables,
        'course': course,
        'semester': semester
    })