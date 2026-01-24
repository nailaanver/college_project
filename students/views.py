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

from django.db.models import Avg
from students.utils.performance_ai import generate_academic_summary
from fees.models import Fee


@login_required(login_url='student-login')
def student_dashboard(request):
    user = request.user

    try:
        student = user.student_profile
    except Student.DoesNotExist:
        return redirect('student-login')

    # ---------------- Attendance ----------------
    total_classes = Attendance.objects.filter(student=student).count()
    present_classes = Attendance.objects.filter(
        student=student,
        status='P'
    ).count()

    attendance_percentage = (
        round((present_classes / total_classes) * 100, 2)
        if total_classes > 0 else 0
    )

    # ---------------- Internals ----------------
    internal_avg = InternalMark.objects.filter(
        student=student,
        status='Approved'
    ).aggregate(avg=Avg('total_internal'))['avg'] or 0

    internal_avg = round(internal_avg, 2)

    academic_summary = generate_academic_summary(
        attendance_percentage,
        internal_avg
    )

    internals_count = InternalMark.objects.filter(student=student).count()
    issued_books = Issue.objects.filter(user=user, status='ISSUED').count()

    # ---------------- ✅ FEES (NEW) ----------------
    pending_fees = Fee.objects.filter(
        student=student,
        is_paid=False
    )

    paid_fees = Fee.objects.filter(
        student=student,
        is_paid=True
    ).order_by('-paid_on')

    # ---------------- Context ----------------
    context = {
        'student': student,
        'attendance_percentage': attendance_percentage,
        'internals_count': internals_count,
        'issued_books': issued_books,
        'academic_summary': academic_summary,

        # ✅ NEW FOR PAYMENT UI
        'pending_fees': pending_fees,
        'paid_fees': paid_fees,
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


from django.contrib import messages
from .models import Student
from .forms import StudentForm

@login_required(login_url='student-login')
def student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('student-dashboard')

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('student-profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = StudentForm(instance=student)

    return render(request, 'student/profile.html', {
        'student': student,
        'form': form
    })
from django.db.models import Count, Q

@login_required(login_url='student-login')
def student_attendance(request):

    # Safety check (optional but recommended)
    if request.user.role != 'student':
        return redirect('student-login')

    student = get_object_or_404(Student, user=request.user)

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
from django.shortcuts import get_object_or_404

@login_required(login_url='student-login')
def student_internal_marks(request):
    student = get_object_or_404(Student, user=request.user)

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


