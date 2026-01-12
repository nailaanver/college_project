from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from students.models import Student, StudentFace
from .face.encode import encode_face
from django.contrib import messages

@login_required(login_url='student-login')
def upload_face(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect('student-dashboard')

    if request.method == 'POST':
        image = request.FILES.get('face_image')

        if not image:
            messages.error(request, "Please upload an image")
            return redirect('upload-face')

        try:
            encoding = encode_face(image)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('upload-face')

        StudentFace.objects.update_or_create(
            student=student,
            defaults={'face_encoding': encoding}
        )

        messages.success(request, "Face registered successfully")
        return redirect('student-dashboard')

    return render(request, 'ai_services/upload_face.html')
