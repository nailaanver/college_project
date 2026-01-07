from django.shortcuts import render,redirect,get_object_or_404

from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from dashboard.models import TimeTable
from django.utils import timezone


@login_required
def attendance_home(request):
    today = date.today().strftime('%A')
    
    timetables = TimeTable.objects.filter(
        teacher = request.user.teacher,
        day= today
    ).order_by('period_number')
    
    return render(request,'attendance/today_timetable.html',{
        'timetables' : timetables
    })
    
# @login_required
# def attendance_home(request):
#     yesterday = (date.today() - timedelta(days=2)).strftime('%A')

#     timetables = TimeTable.objects.filter(
#         teacher=request.user.teacher,
#         day=yesterday
#     ).order_by('period_number')

#     return render(request, 'attendance/today_timetable.html', {
#         'timetables': timetables,
#         'day': yesterday
#     })
from students.models import Student
from .models import Attendance

@login_required
def mark_attendance(request, timetable_id):

    timetable = get_object_or_404(TimeTable, id=timetable_id)

    # ✅ Get students of that course & semester
    students = Student.objects.filter(
        course=timetable.course,
        semester=timetable.semester
    ).order_by('register_number')

    today = timezone.now().date()

    # ❗ Prevent duplicate attendance
    if Attendance.objects.filter(
        subject=timetable.subject,
        period=timetable.period_number,
        date=today
    ).exists():
        return redirect('attendance_summary', timetable.id)

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'A')

            Attendance.objects.create(
                student=student,
                subject=timetable.subject,
                date=date.today(),
                period=timetable.period_number,
                status=status
            )


        return redirect('attendance_summary', timetable.id)

    return render(request, 'attendance/mark.html', {
        'timetable': timetable,
        'students': students
    })
from django.db.models import Count

@login_required
def attendance_summary(request, timetable_id):

    timetable = get_object_or_404(TimeTable, id=timetable_id)
    today = timezone.now().date()

    attendance_qs = Attendance.objects.filter(
        subject=timetable.subject,
        period=timetable.period_number,
        date=today
    ).select_related('student')

    total_students = attendance_qs.count()
    present_count = attendance_qs.filter(status='P').count()
    late_count = attendance_qs.filter(status='L').count()
    absent_count = attendance_qs.filter(status='A').count()

    return render(request, 'attendance/summary.html', {
        'timetable': timetable,
        'attendance': attendance_qs,
        'total_students': total_students,
        'present_count': present_count,
        'late_count': late_count,
        'absent_count': absent_count,
    })

@login_required
def edit_attendance(request, timetable_id):
    timetable = TimeTable.objects.get(id=timetable_id)

    students = Student.objects.filter(
        course=timetable.course,
        semester=timetable.semester
    )

    attendance_qs = Attendance.objects.filter(
        subject=timetable.subject,
        date=date.today(),
        period=timetable.period_number
    )

    attendance_map = {a.student_id: a for a in attendance_qs}

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')

            # 🔴 IMPORTANT FIX
            if not status:
                continue   # skip this student safely

            Attendance.objects.update_or_create(
                student=student,
                subject=timetable.subject,
                date=date.today(),
                period=timetable.period_number,
                defaults={'status': status}
            )

        return redirect('attendance_summary', timetable.id)

    return render(request, 'attendance/edit.html', {
        'timetable': timetable,
        'students': students,
        'attendance_map': attendance_map
    })
