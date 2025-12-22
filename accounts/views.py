from django.shortcuts import render

from django.shortcuts import render, redirect
from students.models import Student
from teachers.models import Teacher


def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        # ---------------- STUDENT LOGIN ----------------
        if role == 'student':
            email = request.POST.get('email')
            dob = request.POST.get('dob')

            try:
                student = Student.objects.get(
                    email=email,
                    date_of_birth=dob
                )
                request.session['role'] = 'student'
                request.session['student_id'] = student.id
                return redirect('student_dashboard')

            except Student.DoesNotExist:
                return render(request, 'login.html', {
                    'error': 'Invalid student login details'
                })

        # ---------------- PARENT LOGIN ----------------
        elif role == 'parent':
            register_number = request.POST.get('register_number')
            parent_name = request.POST.get('parent_name')

            try:
                student = Student.objects.get(
                    register_number=register_number,
                    parent_name__iexact=parent_name
                )
                request.session['role'] = 'parent'
                request.session['student_id'] = student.id
                return redirect('parent_dashboard')

            except Student.DoesNotExist:
                return render(request, 'login.html', {
                    'error': 'Invalid parent login details'
                })

        # ---------------- TEACHER LOGIN ----------------
        elif role == 'teacher':
            email = request.POST.get('email')
            dob = request.POST.get('dob')

            try:
                teacher = Teacher.objects.get(
                    email=email,
                    date_of_birth=dob
                )
                request.session['role'] = 'teacher'
                request.session['teacher_id'] = teacher.id
                return redirect('teacher_dashboard')

            except Teacher.DoesNotExist:
                return render(request, 'login.html', {
                    'error': 'Invalid teacher login details'
                })

    return render(request, 'login.html')
