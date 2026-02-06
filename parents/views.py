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

from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from attendance.models import Attendance
from students.models import Student
from fees.models import Fee
from parents.models import ParentNotification


def parent_dashboard(request):
    if not request.session.get('parent_verified'):
        return redirect('parent_send_otp')

    student_id = request.session.get('parent_student_id')
    student = get_object_or_404(Student, id=student_id)

    parent_user = student.parent
    today = date.today()
    current_semester = student.semester  # ✅ IMPORTANT

    # 🔔 Unread notifications
    unread_notification_count = ParentNotification.objects.filter(
        student=student,
        is_read=False
    ).count()

    # -------------------------
    # ✅ ATTENDANCE (CURRENT SEM ONLY)
    # -------------------------
    today_attendance = Attendance.objects.filter(
        student=student,
        semester=current_semester,
        date=today
    ).order_by('period')

    total_classes = Attendance.objects.filter(
        student=student,
        semester=current_semester
    ).count()

    present_classes = Attendance.objects.filter(
        student=student,
        semester=current_semester,
        status='P'
    ).count()

    attendance_percentage = (
        round((present_classes / total_classes) * 100, 2)
        if total_classes > 0 else 0
    )

    # -------------------------
    # ✅ INTERNAL MARKS (CURRENT SEM ONLY)
    # -------------------------
    internal_marks = (
        InternalMark.objects
        .filter(
            student=student,
            semester=current_semester,
            status='Approved'
        )
        .select_related('subject')
        .order_by('subject__name')
    )

    # -------------------------
    # FEES
    # -------------------------
    pending_fees = Fee.objects.filter(student=student, is_paid=False)
    paid_fees = Fee.objects.filter(student=student, is_paid=True).order_by('-paid_on')

    context = {
        'student': student,
        'parent_user': parent_user,
        'today_attendance': today_attendance,
        'attendance_percentage': attendance_percentage,
        'today': today,
        'student_fees': pending_fees,
        'paid_fees': paid_fees,
        'internal_marks': internal_marks,
        'unread_notification_count': unread_notification_count,
    }

    return render(request, 'parents/parent_dashboard.html', context)

from django.db.models import Count, Q
from collections import defaultdict


def parent_previous_semester(request, semester):
    if not request.session.get('parent_verified'):
        return redirect('parent_send_otp')

    student_id = request.session.get('parent_student_id')
    student = get_object_or_404(Student, id=student_id)

    current_semester = student.semester

    # ❌ Prevent invalid access
    if semester >= current_semester or semester < 1:
        return redirect('parent_dashboard')

    # ---------- ATTENDANCE ✅ (SAME AS STUDENT LOGIC) ----------
    attendance_qs = Attendance.objects.filter(
        student=student,
        subject__semester=semester     # 🔥 THIS IS THE FIX
    ).order_by('date', 'period')

    attendance_matrix = defaultdict(dict)
    for att in attendance_qs:
        attendance_matrix[att.date][att.period] = att.status

    # ---------- INTERNAL MARKS ----------
    internal_marks = InternalMark.objects.filter(
        student=student,
        semester=semester,
        status='Approved'
    ).select_related('subject')

    context = {
        'student': student,
        'semester': semester,
        'attendance_matrix': dict(attendance_matrix),
        'periods': range(1, 8),
        'internal_marks': internal_marks,
    }

    return render(
        request,
        'parents/previous_semester_history.html',
        context
    )

    
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
    
    
# parents/views.py
from parents.models import ParentNotification

def parent_notification_list(request):
    if not request.session.get('parent_verified'):
        return redirect('parent_send_otp')

    student_id = request.session.get('parent_student_id')

    notifications = ParentNotification.objects.filter(
        student_id=student_id
    ).order_by('-created_at')

    notifications.filter(is_read=False).update(is_read=True)

    return render(
        request,
        'parents/parent_notification_list.html',
        {'notifications': notifications}
    )
