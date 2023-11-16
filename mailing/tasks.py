from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from .models import Subscriber
from lynkly import settings
	
@shared_task(bind=True)
def send_mail_func(self):
    users=get_user_model().objects.all()
    users.extend(Subscriber.objects.all())
    for user in users:
        mail_subject=f"Hello {user.username}"
        message="This for joining Linkly services"
        to_email=user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
            )
    return "Task Successfull"

@shared_task(bind=True)
def subscriber_func(self, email):
    mail_subject=f"Hello subscriber!"
    message="Thanks for subscribing Linkly monthly newsletter."
    to_email=email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
        )
    return "Task Successfull"