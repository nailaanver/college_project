from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

def send_payment_receipt(fee):
    student = fee.student
    parent_email = student.parent.email or student.parent_email

    context = {
        'student_name': f"{student.first_name} {student.last_name}",
        'register_number': student.register_number,
        'fee_type': fee.fee_type,
        'amount': fee.amount,
        'payment_id': fee.paypal_order_id,
        'date': timezone.now().strftime("%d %B %Y"),
    }

    html_content = render_to_string('fees/email_receipt.html', context)

    email = EmailMultiAlternatives(
        subject="Fee Payment Receipt",
        body="Your fee payment was successful.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[parent_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()


from datetime import date
from .models import FeeStructure, Fee
from students.models import Student

def generate_fees_for_student(student):
    """
    Generate fees for a student based on course-specific or global FeeStructure.
    """
    # Course-specific fees
    course_fees = FeeStructure.objects.filter(course=student.course)
    # Global fees
    global_fees = FeeStructure.objects.filter(course__isnull=True)
    
    all_fees = list(course_fees) + list(global_fees)
    
    for fee_struct in all_fees:
        # Avoid duplicate fees
        if not Fee.objects.filter(
            student=student,
            fee_type=fee_struct.fee_type,
            semester=fee_struct.semester
        ).exists():
            Fee.objects.create(
                student=student,
                fee_type=fee_struct.fee_type,
                semester=fee_struct.semester,
                amount=fee_struct.amount,
                due_date=date.today()  # Customize this
            )
