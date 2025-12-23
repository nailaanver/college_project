from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from students.models import Student

def student_login(request):
    if request.method == 'POST':
        reg_no = request.POST.get('register_number')
        dob = request.POST.get('dob')

        try:
            student = Student.objects.get(register_number=reg_no)
            user = authenticate(
                request,
                username=student.user.username,
                password=dob.replace('-', '')
            )
            if user:
                login(request, user)
                return redirect('student-dashboard')
        except Student.DoesNotExist:
            pass

        return render(request, 'accounts/student_login.html', {
            'error': 'Invalid details'
        })

    return render(request, 'accounts/student_login.html')

from teachers.models import Teacher

def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        dob = request.POST.get('dob')

        try:
            teacher = Teacher.objects.get(email=email)
            user = authenticate(
                request,
                username=teacher.user.username,
                password=dob.replace('-', '')
            )
            if user:
                login(request, user)
                return redirect('teacher-dashboard')
        except Teacher.DoesNotExist:
            pass

        return render(request, 'accounts/teacher_login.html', {
            'error': 'Invalid details'
        })

    return render(request, 'accounts/teacher_login.html')

from students.models import Student

def parent_login(request):
    if request.method == 'POST':
        reg_no = request.POST.get('register_number')
        parent_name = request.POST.get('parent_name')

        try:
            student = Student.objects.get(
                register_number=reg_no,
                parent_name__iexact=parent_name
            )
            user = authenticate(
                request,
                username=student.user.username,
                password=reg_no
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
