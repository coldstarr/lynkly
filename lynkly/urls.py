from django.contrib import admin
from django.urls import path, include
from authentication.views import login, signup, logout
from urlhandler.views import dashboard, generate, home, deleteurl
from pricing.views import pricing
from contact.views import contact, contactthanks
from payments.views import payment, payment_success

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('payment/', payment, name="payment"),
    path('success/', payment_success, name="success"),
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),
    path('logout/', logout, name="logout"),
    path('app.dashboard/', dashboard, name="app.dashboard"),
    path('generate/', generate, name="generate"),
    path('deleteurl/', deleteurl, name="deleteurl"),
    path('<str:query>', home, name="home"),
    path('pricing/', pricing, name="pricing"),
    path('contact/', contact, name="contact"),
    path('thanks/', contactthanks, name="thanks"),
    path('',include('mailing.urls'))
]
