from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from .tasks import send_mail_func, subscriber_func
from django.contrib import messages
from .models import Subscriber

# Create your views here.
def send_mail_to_all_users(request):
    send_mail_func.delay()
    return HttpResponse("Email has beed Sent Successfully")

def scheduledmail(request):
    schedule,created=CrontabSchedule.objects.get_or_create(hour=20,minute=45)
    #we need to give name dynamically. now i am manually adding like mail_task_1
    task=PeriodicTask.objects.create(crontab=schedule,
    name="mail_task_"+"6",task='mailfireapp.tasks.send_mail_func')
    return HttpResponse("success")

def subscriber(request):
  if request.method == 'POST':
    email = request.POST.get('newsletter1')
    print(email, flush=True)
    
    if email:
        # Check if the user is already subscribed
        if Subscriber.objects.filter(email=email).exists():
            messages.success(request, "You are already subscribed.")
            return redirect('/')

        # Pass the email address to the subscriber_func() Celery task as a keyword argument
        subscriber_func.delay(email=email)

        # Create a new subscriber record
        new_subscriber = Subscriber(email=email)
        new_subscriber.save()
    
        messages.success(request, "Subscription successful!")
    return redirect('/')
  else:
    return redirect('/')
