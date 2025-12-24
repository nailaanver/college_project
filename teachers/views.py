from django.shortcuts import render,redirect
from teachers.models import Teacher
from django.contrib.auth.decorators import login_required

@login_required
def teacher_dashboard(request):
    return render(request, 'teachers/dashboard.html')

