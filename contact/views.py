from django.shortcuts import render

# Create your views here.
def contact(request):
    return render(request, 'contact.html')

def contactthanks(request):
    return render(request, 'contactthanks.html')