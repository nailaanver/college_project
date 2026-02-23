from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
import paypalrestsdk
from .models import Fee
from students.models import Student
from .utils import send_payment_receipt
from django.contrib.auth.decorators import login_required
from fees.models import TeacherLibraryFine

# Custom decorator for OTP-based parent login
from functools import wraps
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def fee_payer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # Case 1: Student logged in (normal auth)
        if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
            request.paid_by = 'student'
            request.student = request.user.student_profile
            return view_func(request, *args, **kwargs)

        # Case 2: Parent OTP session
        if request.session.get('parent_verified'):
            request.paid_by = 'parent'
            student_id = request.session.get('parent_student_id')
            request.student = get_object_or_404(Student, id=student_id)
            return view_func(request, *args, **kwargs)

        # Unauthorized
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    return wrapper


# -------------------------------
# CREATE PAYPAL PAYMENT
# -------------------------------
@fee_payer_required
def create_paypal_payment(request, fee_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    student = request.student
    paid_by = request.paid_by

    fee = get_object_or_404(Fee, id=fee_id, student=student, is_paid=False)

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(
                f"/api/fees/execute/{fee.id}/"
            ),
            "cancel_url": request.build_absolute_uri(
                "/parent/dashboard/" if paid_by == 'parent' else "/student/dashboard/"
            ),
        },
        "transactions": [{
            "amount": {"total": str(fee.amount), "currency": "USD"},
            "description": f"{fee.fee_type} payment",
        }],
    })

    if payment.create():
        fee.paypal_order_id = payment.id
        fee.save()
        for link in payment.links:
            if link.rel == "approval_url":
                return JsonResponse({"approval_url": link.href})

    return JsonResponse({"error": payment.error}, status=400)

# -------------------------------
# EXECUTE PAYPAL PAYMENT
# -------------------------------
from notifications.models import Notification
from parents.models import ParentNotification

# -------------------------------
# EXECUTE PAYPAL PAYMENT
# -------------------------------
@fee_payer_required
def execute_paypal_payment(request, fee_id):

    student = request.student
    paid_by = request.paid_by

    fee = get_object_or_404(Fee, id=fee_id, student=student)

    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    if not payment_id or not payer_id:
        return redirect(
            "/parent/dashboard/?payment=failed"
            if paid_by == 'parent'
            else "/student/dashboard/?payment=failed"
        )

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):

        # ✅ Update fee status
        fee.is_paid = True
        fee.paid_by = paid_by
        fee.paid_on = timezone.now()
        fee.save()
        
        # ===============================
        # 📚 LIBRARY FINE SYNC
        # ===============================
        if fee.fee_type == "LIBRARY":
            from library.models import Issue
            Issue.objects.filter(
                user=student.user,
                fine_paid=False
            ).update(fine_paid=True)


        send_payment_receipt(fee)

        # ===============================
        # 🔔 STUDENT NOTIFICATION
        # ===============================
        if student.user:
            Notification.objects.create(
                recipient=student.user,
                title="✅ Fee Payment Successful",
                message=(
                    f"Your {fee.fee_type} fee of ₹{fee.amount} "
                    f"has been successfully paid."
                ),
                notification_type="FEES",
                reference_id=fee.id
            )

        # ===============================
        # 🔔 PARENT NOTIFICATION
        # ===============================
        if student.parent:
            ParentNotification.objects.create(
                student=student,
                title="✅ Fee Payment Successful",
                message=(
                    f"{student.first_name}'s {fee.fee_type} fee of "
                    f"₹{fee.amount} has been successfully paid."
                )
            )

        return redirect(
            "/parent/dashboard/?payment=success"
            if paid_by == 'parent'
            else "/student/dashboard/?payment=success"
        )

    return redirect(
        "/parent/dashboard/?payment=failed"
        if paid_by == 'parent'
        else "/student/dashboard/?payment=failed"
    )


