# views.py
from django.shortcuts import render, redirect
from students.models import Student
from django.contrib.auth.decorators import login_required

def parent_dashboard(request):
    if not request.session.get('parent_verified'):
        return redirect('parent_send_otp')

    student_id = request.session.get('parent_student_id')
    student = Student.objects.get(id=student_id)

    return render(request, 'parents/parent_dashboard.html', {
        'student': student
    })
    
def parent_logout(request):
    request.session.flush()
    return redirect('parent_send_otp')


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

def parent_send_otp(request):
    if request.method == 'POST':
        reg_no = request.POST.get('register_number').strip()
        parent_email = request.POST.get('parent_email').strip()

        student = Student.objects.filter(register_number=reg_no, parent_email__iexact=parent_email).first()

        if not student:
            return render(request, 'accounts/parent_send_otp.html', {
                'error': 'Invalid Register Number or Parent Email'
            })

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        student.otp = otp
        student.otp_created_at = timezone.now()
        student.save()

        # Send OTP
        send_mail(
            subject='Your OTP for Parent Login',
            message=f'Hello! Your OTP is {otp}. It is valid for 5 minutes.',
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[parent_email],
        )

        # Store student id in session
        request.session['parent_student_id'] = student.id
        return redirect('parent_verify_otp')

    return render(request, 'accounts/parent_send_otp.html')


def parent_verify_otp(request):
    student_id = request.session.get('parent_student_id')

    if not student_id:
        return redirect('parent_send_otp')

    student = Student.objects.filter(id=student_id).first()
    if not student:
        return redirect('parent_send_otp')

    if request.method == 'POST':
        otp_input = request.POST.get('otp').strip()

        if student.otp != otp_input:
            return render(request, 'accounts/parent_verify_otp.html', {
                'error': 'Incorrect OTP'
            })

        if timezone.now() > student.otp_created_at + timedelta(minutes=5):
            return render(request, 'accounts/parent_verify_otp.html', {
                'error': 'OTP expired'
            })

        # ✅ OTP VERIFIED
        request.session['parent_verified'] = True   # 🔴 THIS WAS MISSING
        request.session['parent_student_id'] = student.id

        student.otp = None
        student.save()

        return redirect('parent_dashboard')  # ✅ fixed name

    return render(request, 'accounts/parent_verify_otp.html')
