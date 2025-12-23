from django.shortcuts import render, redirect
from .models import Student
from django.contrib.auth.decorators import login_required

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

@login_required
def student_dashboard(request):
    return render(request,'student/dashboard.html')