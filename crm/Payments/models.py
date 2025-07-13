from django.db import models

# Create your models here.

from students.models import BaseClass

class PaymentStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'

class Payments(BaseClass):
    student = models.OneToOneField(
        "students.Students",
        on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.first_name} {self.student.batch.name}"
    class Meta:
        verbose_name = "Payments"
        verbose_name_plural = "Payments"

class Transactions(BaseClass):
    payment = models.ForeignKey(
        Payments,
        on_delete=models.CASCADE,
        choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)
    rzp_order_id = models.SlugField()
    amount = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING)
    rzp_payment_id = models.SlugField(null=True, blank=True)
    rzp_signature = models.TextField(null=True, blank=True) 
    transaction_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id} for {self.payment.student.first_name}{self.payment.student.batch.name} - {self.status}"
    
    class Meta:
        verbose_name = "Transactions"
        verbose_name_plural = "Transactions"