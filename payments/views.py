from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import stripe

# Create your views here.

@login_required(login_url='/login/')
def payment(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1O6yz6SDz9RXgA45M7OEedCd',
            'quantity':1
        }],
        mode='subscription',
        success_url = request.build_absolute_uri(reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = request.build_absolute_uri(reverse('payment'))
    )
    
    context = {
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'payment.html', context)

def payment_success(request):
   # Here will use celery
   return render(request, 'payment_success.html')