from django.shortcuts import render,redirect

from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from dashboard.models import TimeTable

# @login_required
# def attendance_home(request):
#     today = date.today().strftime('%A')
    
#     timetables = TimeTable.objects.filter(
#         teacher = request.user.teacher,
#         day= today
#     ).order_by('period_number')
    
#     return render(request,'attendance/today_timetable.html',{
#         'timetables' : timetables
#     })
    
@login_required
def attendance_home(request):
    yesterday = (date.today() - timedelta(days=1)).strftime('%A')

    timetables = TimeTable.objects.filter(
        teacher=request.user.teacher,
        day=yesterday
    ).order_by('period_number')

    return render(request, 'attendance/today_timetable.html', {
        'timetables': timetables,
        'day': yesterday
    })
from students.models import Student
from .models import Attendance

@login_required
def mark_attendance(request, timetable_id):
    timetable = TimeTable.objects.get(id=timetable_id)
    
    students = Student.objects.filter(
        course=timetable.course,
        semester=timetable.semester
    )

    if request.method == 'POST':
        present = request.POST.getlist('present')
        late = request.POST.getlist('late')

        for student in students:
            status = 'Absent'
            if str(student.id) in present:
                status = 'Present'
            elif str(student.id) in late:
                status = 'Late'

            Attendance.objects.create(
                student=student,
                timetable=timetable,
                date=date.today(),
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
    records = Attendance.objects.filter(
        timetable_id=timetable_id,
        date=date.today()
    )

    summary = records.values('status').annotate(count=Count('id'))

    return render(request, 'attendance/summary.html', {
        'summary': summary
    })
