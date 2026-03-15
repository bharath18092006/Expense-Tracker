from django.conf import settings
from django.core.mail import send_mail


def send_expense_alert(user_email, limit, spent):
    subject = "ExpenseWise Alert: Daily Limit Exceeded"
    message = f"""
Hello,

Your daily spending limit has been exceeded.

Daily Limit: Rs.{limit}
Today's Spending: Rs.{spent}

Please review your expenses in ExpenseWise.

Thank you,
ExpenseWise System
"""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
