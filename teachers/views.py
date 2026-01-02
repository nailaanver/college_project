from django.shortcuts import render,redirect
from teachers.models import Teacher
from django.contrib.auth.decorators import login_required
from dashboard.models import TimeTable

@login_required
def teacher_dashboard(request):
    return render(request, 'teachers/dashboard.html')


# teachers/views.py
from .models import Teacher
from django.contrib import messages

@login_required
def teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    
    if request.method == 'POST':
        teacher.department = request.POST.get('department')
        teacher.contact_number = request.POST.get('contact_number')
        if 'profile_picture' in request.FILES:
            teacher.profile_picture = request.FILES['profile_picture']
        teacher.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('teacher_profile')
    
    return render(request, 'teachers/teacher_profile.html', {'teacher': teacher})

@login_required
def teacher_timetable(request):
    teacher = request.user.teacher

    timetables = TimeTable.objects.filter(
        teacher=teacher
    ).select_related('subject', 'teacher')

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = sorted(
        timetables.values_list('period_number', flat=True).distinct()
    )

    return render(request, 'teachers/teacher_timetable.html', {
        'timetables': timetables,
        'days': days,
        'periods': periods,
    })

    
from datetime import datetime

@login_required
def teacher_today_timetable(request):
    today = datetime.today().strftime('%A')

    timetable = TimeTable.objects.filter(
        teacher=request.user.teacher,
        day=today
    ).order_by('period_number')

    return render(request, 'teachers/teacher_today.html', {
        'timetable': timetable
    })

