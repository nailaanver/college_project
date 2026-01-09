from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
import paypalrestsdk
from .models import Fee
from students.models import Student
from .utils import send_payment_receipt

# Custom decorator for OTP-based parent login
from functools import wraps
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def parent_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('parent_verified'):
            return view_func(request, *args, **kwargs)
        # If AJAX/API, return JSON error
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return redirect('parent_send_otp')
    return wrapper

# -------------------------------
# CREATE PAYPAL PAYMENT
# -------------------------------
@parent_login_required
def create_paypal_payment(request, fee_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    # Get student from session
    student_id = request.session.get('parent_student_id')
    student = get_object_or_404(Student, id=student_id)

    fee = get_object_or_404(Fee, id=fee_id, student=student, is_paid=False)

    # Create PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(
    f"/api/fees/execute/{fee.id}/"
),

            "cancel_url": request.build_absolute_uri("/parent/dashboard/"),
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
@parent_login_required
def execute_paypal_payment(request, fee_id):
    # Get student from session
    student_id = request.session.get('parent_student_id')
    student = get_object_or_404(Student, id=student_id)

    fee = get_object_or_404(Fee, id=fee_id, student=student)

    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    if not payment_id or not payer_id:
        return redirect("/parent/dashboard/?payment=failed")

    # Find PayPal payment
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        fee.is_paid = True
        fee.paid_on = timezone.now()
        fee.save()
        # Send receipt email (optional)
        send_payment_receipt(fee)
        return redirect("/parent/dashboard/?payment=success")

    return redirect("/parent/dashboard/?payment=failed")
