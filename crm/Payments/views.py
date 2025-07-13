from django.shortcuts import render,redirect
from decimal import Decimal, ROUND_HALF_UP
# Create your views here.
from django.views.generic import View
from .models import Payments, Transactions
import razorpay
from decouple import config
from django.db import transaction
import datetime


class StudentPaymentView(View):
    def get(self, request, *args, **kwargs):
        try:
            payment = Payments.objects.get(student__profile=request.user)
        except Payments.DoesNotExist:
            return render(request, "errorpages/error-404.html")
        data = {
            "payment": payment,
        }
        return render(request, "payments/student-payment-details.html", context=data)


class RazorpayView(View):
    def get(self, request, *args, **kwargs):
        print("CLIENT ID:", config("RZP_CLIENT_ID"))
        print("SECRET:", config("RZP_CLIENT_SECRET"))
        with transaction.atomic():
            payment_obj = Payments.objects.get(student__profile=request.user)
            client = razorpay.Client(
                auth=(config("RZP_CLIENT_ID"), config("RZP_CLIENT_SECRET"))
            )
            amount = int(
                Decimal(payment_obj.amount).quantize(Decimal("0.01"), ROUND_HALF_UP)
                * 100
            )
            data = {
                "amount": amount,
                "currency": "INR",
                "receipt": f"receipt_{payment_obj.id}",
                "notes": {
                    "student_id": payment_obj.student.id,
                    "payment_id": payment_obj.id,
                },
            }
            payment = client.order.create(data=data)
            order_id = payment.get("id")
            amount = payment.get("amount")
            Transactions.objects.create(
                payment=payment_obj, rzp_order_id=order_id, amount=amount
            )
            data = {
                "order_id": order_id,
                "amount": amount,
                "RZP_CLIENT_ID": config("RZP_CLIENT_ID"),
            }
            print("Order ID:", order_id)
            print("Amount:", amount)
            return render(request, "payments/razorpay-page.html", context=data)

class PaymentVerifyView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        rzp_order_id = data.get("razorpay_order_id")
        rzp_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")
        transaction_obj = Transactions.objects.filter(rzp_order_id=rzp_order_id).first()
        transaction_obj.rzp_payment_id = rzp_payment_id
        transaction_obj.rzp_signature = razorpay_signature
        client = razorpay.Client(
            auth=("rzp_test_WxlwtarV5KteQU", "VgpYWbS08kBH3C7CYVypp1Sy")
        )
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": rzp_order_id,
                "razorpay_payment_id": rzp_payment_id,
                "razorpay_signature": razorpay_signature
            })
            transaction_obj.status = "success"
            transaction_obj.transaction_at = datetime.datetime.now()
            transaction_obj.payment.status = "success"
            transaction_obj.payment.paid_at = datetime.datetime.now()
            transaction_obj.payment.save()
            transaction_obj.save()
        except:
            transaction_obj.rzp_payment_id = rzp_payment_id
            transaction_obj.rzp_signature = razorpay_signature
            transaction_obj.save()
        return redirect("student-payment-details")