from celery import shared_task
from accounts.models import UserProfile
from tender.models import Tender
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.settings import EMAIL_HOST_USER
from datetime import datetime

from datetime import datetime, timedelta


@shared_task
def send_tender_email():
    users = UserProfile.objects.all()
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday_noon = datetime.now().replace(hour=12, minute=0, second=0,
                                            microsecond=0) - timedelta(days=1)
    today_noon = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

    for user in users:
        tenders = Tender.objects.filter(created_date__range=(yesterday_noon, today_noon)).filter(
            tender_type="TENDER"
        ).filter(
            project_type__in=user.project_type.all()
        )
        # Check if tenders exist for the user
        if tenders.exists():
            # Assuming you have a template for the email
            email_subject = f"TENDER NOTICE {today}"
            email_template = 'frontend/tender_email_template.html'
            context = {'user': user, 'tenders': tenders}
            html_message = render_to_string(email_template, context)
            plain_message = strip_tags(html_message)
            send_mail(
                email_subject,
                plain_message,
                EMAIL_HOST_USER,  # Sender's email address
                [user.user.email],  # List of recipients
                html_message=html_message,
            )
