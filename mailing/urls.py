from django.urls import path, include
from . import views

urlpatterns = [
    path('mailing/', views.send_mail_to_all_users,name='mailing'),
    path('scheduledmail/', views.scheduledmail, name="scheduledmail"),
    path('subscribe/', views.subscriber, name="subscribe")   
]