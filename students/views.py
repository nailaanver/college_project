from django.shortcuts import render, redirect
from .models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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

@login_required(login_url='student-login')
def student_dashboard(request):
    return render(request,'student/dashboard.html')


def student_logout(request):
    logout(request)
    return redirect('role_login')