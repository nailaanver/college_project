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
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print("EMAIL:", email)
        print("PASSWORD:", password)

        user = authenticate(request, username=email, password=password)

        print("AUTH USER:", user)

        if user:
            print("ROLE:", user.role)
            print("HAS STUDENT:", hasattr(user, 'student'))

            login(request, user)
            return redirect('student-dashboard')

        print("AUTH FAILED")

    return render(request, 'accounts/student_login.html')



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from teachers.models import Teacher
from django.contrib.auth import get_user_model

User = get_user_model()

def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use authenticate
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Check if user has a Teacher profile
            try:
                teacher = Teacher.objects.get(user=user)
                login(request, user)
                return redirect('teacher-dashboard')
            except Teacher.DoesNotExist:
                messages.error(request, "You are not registered as a teacher.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/teacher_login.html')





from django.contrib.auth import authenticate, login

def parent_login(request):
    if request.method == 'POST':
        reg_no = request.POST.get('register_number')

        try:
            parent_user = User.objects.get(
                username=f"{reg_no}_parent",
                role='parent'
            )

            user = authenticate(
                request,
                username=parent_user.username,
                password=reg_no  # must MATCH set_password()
            )

            if user is not None:
                login(request, user)
                return redirect('parent-dashboard')

        except User.DoesNotExist:
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

from django.shortcuts import redirect

def role_redirect(request):
    if hasattr(request.user, 'student'):
        return redirect('student-dashboard')
    elif hasattr(request.user, 'teacher'):
        return redirect('teacher-dashboard')
    elif hasattr(request.user, 'parent'):
        return redirect('parent-dashboard')
    else:
        return redirect('role-login')
