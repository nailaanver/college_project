from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from students.models import Student
from teachers.models import Teacher


from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.utils import timezone

from students.models import Student

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db.models import Q

# views.py
import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Q





def student_login(request):
    if request.method == 'POST':
        reg_no = request.POST.get('register_number')
        password = request.POST.get('password')  # DOB as YYYYMMDD

        user = authenticate(
            request,
            username=reg_no,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('student-dashboard')

        return render(request, 'accounts/student_login.html', {
            'error': 'Invalid Register Number or Password'
        })

    return render(request, 'accounts/student_login.html')

def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')  # DOB as YYYYMMDD

        try:
            teacher = Teacher.objects.get(email=email)

            user = authenticate(
                request,
                username=teacher.user.username,
                password=password
            )

            if user:
                login(request, user)
                return redirect('teacher-dashboard')

        except Teacher.DoesNotExist:
            pass

        return render(request, 'accounts/teacher_login.html', {
            'error': 'Invalid email or password'
        })

    return render(request, 'accounts/teacher_login.html')





def parent_login(request):
    if request.method == 'POST':
        reg_no = request.POST.get('register_number')
        parent_name = request.POST.get('parent_name')

        try:
            student = Student.objects.get(
            Q(register_number=reg_no) &
            (Q(father_name__iexact=parent_name) | Q(mother_name__iexact=parent_name))
        )
            user = authenticate(
                request,
                username=student.user.username,
                password=reg_no  # assuming register_number is used as password
            )
            if user:
                login(request, user)
                return redirect('parent-dashboard')
        except Student.DoesNotExist:
            pass

        return render(request, 'accounts/parent_login.html', {
            'error': 'Invalid details'
        })

    return render(request, 'accounts/parent_login.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect('admin-dashboard')

        return render(request, 'accounts/admin_login.html', {
            'error': 'You are not authorized as admin'
        })

    return render(request, 'accounts/admin_login.html')


def role_login(request):
    return render(request, 'accounts/role_login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('home')   # or home / admin-login

