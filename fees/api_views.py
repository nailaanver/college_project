from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Fee
from .utils import send_payment_receipt
import paypalrestsdk
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from students.models import Student
from django.shortcuts import redirect



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import paypalrestsdk
from .models import Fee
from students.models import Student
from .utils import send_payment_receipt

@method_decorator(csrf_exempt, name='dispatch')
class CreatePaypalPaymentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, fee_id):
        parent = request.user
        student = get_object_or_404(Student, parent=parent)
        fee = get_object_or_404(Fee, id=fee_id, student=student, is_paid=False)

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": f"http://127.0.0.1:8000/api/fees/execute/{fee.id}/",
                "cancel_url": "http://127.0.0.1:8000/parent/dashboard/"
            },
            "transactions": [{
                "amount": {
                    "total": str(fee.amount),
                    "currency": "USD"
                },
                "description": f"{fee.fee_type} payment"
            }]
        })

        if payment.create():
            fee.paypal_order_id = payment.id
            fee.save()
            for link in payment.links:
                if link.rel == "approval_url":
                    return Response({"approval_url": link.href})
        else:
            return Response({"error": payment.error}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ExecutePaypalPaymentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, fee_id):
        parent = request.user
        student = get_object_or_404(Student, parent=parent)
        fee = get_object_or_404(Fee, id=fee_id, student=student)

        payment_id = request.GET.get("paymentId")
        payer_id = request.GET.get("PayerID")

        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            fee.is_paid = True
            fee.save()
            send_payment_receipt(fee)
            return Response({"success": True})
        return Response({"error": "Payment failed"}, status=400)


class FeeListAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = []

    def get(self, request):
        student_id = request.session.get('parent_student_id')
        student = Student.objects.get(id=student_id)

        fees = Fee.objects.filter(student=student)
        data = []

        for fee in fees:
            data.append({
                "id": fee.id,
                "fee_type": fee.fee_type,
                "amount": str(fee.amount),
                "is_paid": fee.is_paid,
            })

        return Response(data)
