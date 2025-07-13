from .models import Payments
from django.utils import timezone
import threading
from students.utility import send_email
from apscheduler.schedulers.background import BackgroundScheduler

def remainder_email():
    """
    Function to send remainder email to students who have not paid their fees.
    This function is run as a cron job.
    """
    current_date = timezone.now().date()
    five_days_ago = current_date - timezone.timedelta(days=5)
    pending_payments = Payments.objects.filter(
        transactions__status = "Pending", student__join_date__lte=five_days_ago
    ).distinct()
    if pending_payments.exists():
        for payment in pending_payments:
            subject = "Fee Payment Reminder"
            recipient_list = [payment.student.email]
            template = "email/payment-remainder_email.html"
            context = {
                "name": f"{payment.student.first_name} {payment.student.second_name}",
            }
            thread = threading.Thread(
                target=send_email, args=(subject, template, context, recipient_list)
            )
            thread.start()
            print(f"Remainder email sent to {payment.student.email}")
            send_email(subject, template, context, recipient_list)
            
def scheduler_start():
    """
    Function to start the scheduler for sending remainder emails.
    This function is run as a cron job.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(remainder_email, 'cron', hour=10, minute=0)  # Runs every day at 10:00 AM
    scheduler.start()
    print("Scheduler started for sending remainder emails.")