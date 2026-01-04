from django.shortcuts import render
from django.utils import timezone
from dashboard.models import TimeTable
from students.models import Student
from attendance.models import Attendance

def teacher_dashboard(request):
    teacher = request.user.teacher
    today_name = timezone.now().strftime('%A')

    todays_timetable = TimeTable.objects.filter(
        teacher=teacher,
        day=today_name
    )

    return render(request, 'teachers/dashboard.html', {
        'todays_timetable': todays_timetable
    })

# teachers/views.py
from .models import Teacher
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Teacher

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Teacher
from .forms import UserForm, TeacherForm

@login_required
def teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        teacher_form = TeacherForm(request.POST, request.FILES, instance=teacher)

        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save()
            messages.success(request, "Profile updated successfully!")
            # Redirect to dashboard after update
            return redirect('teacher-dashboard')  # change this to your dashboard URL name
    else:
        user_form = UserForm(instance=request.user)
        teacher_form = TeacherForm(instance=teacher)

    return render(request, 'teachers/teacher_profile.html', {
        'user_form': user_form,
        'teacher_form': teacher_form
    })




@login_required
def teacher_timetable(request):
    teacher = request.user.teacher

    timetables = TimeTable.objects.filter(
        teacher=teacher
    ).select_related('subject', 'teacher')

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', ]
    periods = sorted(
        timetables.values_list('period_number', flat=True).distinct()
    )

    return render(request, 'teachers/teacher_timetable.html', {
        'timetables': timetables,
        'days': days,
        'periods': periods,
    })



