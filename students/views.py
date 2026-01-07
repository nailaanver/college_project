from django.shortcuts import render, redirect
from .models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from attendance.models import Attendance
from internal_marks.models import InternalMark
from dashboard.models import TimeTable

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from attendance.models import Attendance
from internal_marks.models import InternalMark
from library.models import Issue

@login_required(login_url='student-login')
def student_dashboard(request):
    user = request.user

    try:
        student = user.student_profile   # ✅ FIXED
    except Student.DoesNotExist:
        return redirect('student-login')  # or show error page

    total_classes = Attendance.objects.filter(student=student).count()
    present_classes = Attendance.objects.filter(
        student=student,
        status='P'
    ).count()

    attendance_percentage = (
        round((present_classes / total_classes) * 100, 2)
        if total_classes > 0 else 0
    )

    internals_count = InternalMark.objects.filter(student=student).count()
    issued_books = Issue.objects.filter(user=user, status='ISSUED').count()

    context = {
        'student': student,
        'attendance_percentage': attendance_percentage,
        'internals_count': internals_count,
        'issued_books': issued_books,
    }
    return render(request, 'student/dashboard.html', context)



def upload_profile_photo(request):
    if request.session.get('role') != 'student':
        return redirect('login')

    student = Student.objects.get(id=request.session['student_id'])

    if request.method == 'POST':
        student.profile_photo = request.FILES.get('profile_photo')
        student.save()
        return redirect('student_dashboard')

    return render(request, 'students/upload_photo.html', {
        'student': student
    })




def student_logout(request):
    logout(request)
    return redirect('role_login')


@login_required(login_url='student-login')
def student_profile(request):
    student = request.user.student
    return render(request, 'student/profile.html', {'student': student})


from django.db.models import Count, Q

@login_required(login_url='student-login')
def student_attendance(request):
    student = request.user.student

    attendance = Attendance.objects.filter(student=student)

    subject_wise = attendance.values(
        'subject__name'
    ).annotate(
        total=Count('id'),
        present=Count('id', filter=Q(status='P'))
    )

    for s in subject_wise:
        s['percentage'] = round(
            (s['present'] / s['total']) * 100, 2
        ) if s['total'] > 0 else 0

    return render(request, 'student/attendance.html', {
        'subject_wise': subject_wise
    })


@login_required(login_url='student-login')
def student_internal_marks(request):
    student = request.user.student

    marks = InternalMark.objects.filter(
        student=student,
        status='Approved'
    )

    return render(request, 'student/internal_marks.html', {
        'marks': marks
    })


from dashboard.models import TimeTable

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from dashboard.models import TimeTable

# students/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
from dashboard.models import TimeTable
@login_required(login_url='student-login')
def student_timetable(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('student-dashboard')

    timetables = TimeTable.objects.filter(
        course=student.course,
        semester=student.semester
    ).select_related('subject', 'teacher').order_by('day', 'period_number')

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = range(1, 8)  # Period 1 to 7

    return render(request, 'student/timetable.html', {
        'student': student,
        'timetables': timetables,
        'days': days,
        'periods': periods,
    })


