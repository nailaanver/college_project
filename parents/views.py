# views.py
from django.shortcuts import render, redirect
from students.models import Student
from django.contrib.auth.decorators import login_required
from internal_marks.models import InternalMark


from datetime import date
from django.shortcuts import render, redirect
from attendance.models import Attendance
from students.models import Student

from fees.models import Fee

def parent_dashboard(request):
    if not request.session.get('parent_verified'):
        return redirect('parent_send_otp')

    student_id = request.session.get('parent_student_id')
    student = Student.objects.get(id=student_id)
    parent_user = student.parent  # User object (parent)
    today = date.today()

    # Attendance
    today_attendance = Attendance.objects.filter(
        student=student,
        date=today
    ).order_by('period')

    total_classes = Attendance.objects.filter(student=student).count()
    present_classes = Attendance.objects.filter(
        student=student,
        status='P'
    ).count()
    attendance_percentage = (
        (present_classes / total_classes) * 100
        if total_classes > 0 else 0
    )

    # Fees
    student_fees = Fee.objects.filter(student=student, is_paid=False)

    return render(request, 'parents/parent_dashboard.html', {
        'student': student,
        'parent_user': parent_user,
        'today_attendance': today_attendance,
        'attendance_percentage': attendance_percentage,
        'today': today,
        'student_fees': student_fees,   # <-- send fees to template
    })



# def parent_dashboard(request):
#     if not request.session.get('parent_verified'):
#         return redirect('parent_send_otp')

#     student_id = request.session.get('parent_student_id')
#     student = Student.objects.get(id=student_id)

#     return render(request, 'parents/parent_dashboard.html', {
#         'student': student
#     })
    
def parent_logout(request):
    request.session.flush()
    return redirect('parent_send_otp')


from datetime import timedelta


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

# @login_required
# def admin_parent_list(request):
#     if not request.user.is_superuser:
#         return redirect('login')

#     parents = Parent.objects.select_related('student', 'user')

#     return render(request, 'admin/parent_list.html', {
#         'parents': parents
#     })



from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance

@login_required
def parent_today_attendance(request):
    # get student linked to logged-in parent
    student = request.user.parent_student

    today = date.today()

    attendance_list = Attendance.objects.filter(
        student=student,
        date=today
    ).order_by('period')

    return render(request, "parents/today_attendance.html", {
        "student": student,
        "attendance_list": attendance_list,
        "today": today,
    })


from django.db.models import Count, Q

@login_required
def parent_attendance_report(request):
    student = request.user.parent_student

    attendance = Attendance.objects.filter(student=student)

    report = attendance.values('subject__name').annotate(
        total=Count('id'),
        present=Count('id', filter=Q(status='P'))
    )

    for r in report:
        r['percentage'] = (r['present'] / r['total']) * 100 if r['total'] else 0

    return render(request, "parent/attendance_report.html", {
        "student": student,
        "report": report,
    })



def parent_internal_marks(request):
    # OTP verification check
    if not request.session.get('parent_verified'):
        return redirect('parent_send_otp')

    # Get student from session
    student_id = request.session.get('parent_student_id')
    student = Student.objects.get(id=student_id)

    # Get internal marks
    internal_marks = InternalMark.objects.filter(student=student)

    return render(request, 'parents/parent_internal_marks.html', {
        'student': student,
        'internal_marks': internal_marks
    })
    