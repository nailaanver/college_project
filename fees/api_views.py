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



@method_decorator(csrf_exempt, name='dispatch')
class CreatePaypalPaymentAPI(APIView):

    def post(self, request, fee_id):

        # ✅ Parent session check
        student_id = request.session.get('parent_student_id')
        if not student_id:
            return Response(
                {"error": "Parent session expired"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        student = Student.objects.get(id=student_id)

        try:
            fee = Fee.objects.get(id=fee_id, student=student, is_paid=False)
        except Fee.DoesNotExist:
            return Response(
                {"error": "Invalid fee"},
                status=status.HTTP_404_NOT_FOUND
            )

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": f"http://localhost:8000/api/fees/execute/{fee.id}/",
                "cancel_url": f"http://localhost:8000/parent/dashboard/",
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
            fee.paypal_order_id = payment.id   # ✅ CREATED HERE
            fee.save()

            for link in payment.links:
                if link.rel == "approval_url":
                    return Response({"approval_url": link.href})

        return Response(
            {"error": payment.error},
            status=status.HTTP_400_BAD_REQUEST
        )




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

    
from students.models import Student



        
class ExecutePaypalPaymentAPI(APIView):

    def get(self, request, fee_id):

        student_id = request.session.get('parent_student_id')
        if not student_id:
            return Response({"error": "Session expired"}, status=401)

        student = Student.objects.get(id=student_id)
        fee = Fee.objects.get(id=fee_id, student=student)

        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')

        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            fee.is_paid = True
            fee.paypal_order_id = payment_id
            fee.save()

            send_payment_receipt(fee)

            return redirect('/parent/dashboard/')

        return Response({"error": "Payment failed"}, status=400)
