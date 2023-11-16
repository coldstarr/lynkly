from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django_redis import get_redis_connection

def tearDown():
    get_redis_connection("default").flushall()

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('/app.dashboard')

def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            # handle login
            if request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email = request.POST['email'])
                    auth.login(request, user)
                    if request.POST['next'] != '':
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('/')
                except User.DoesNotExist:
                    return render(request, 'login.html', {'error': "User Doesn't Exist"}) 
            else:
                return render(request, 'login.html', {'error': "Empty Fields"}) 
        else:
            return render(request, 'login.html')
    else:
        return redirect('/app.dashboard')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            try:
                if request.POST['password'] == request.POST['password2']:
                    if request.POST['username'] and request.POST['email'] and request.POST['password']:
                        try:
                            user = User.objects.get(email = request.POST['email'])
                            return render(request, 'signup.html', {'error': "User Already Exists"})
                        except User.DoesNotExist:
                            User.objects.create_user(
                                username = request.POST['username'],
                                email = request.POST['email'],
                                password = request.POST['password']
                            )
                            messages.success(request, "Signup Successful <br> Login Here")
                            return redirect(login)
                    else:
                        return render(request, 'signup.html', {'error': "Empty Fields"})
                else:
                    return render(request, 'signup.html', {'error': "Password's Don't Match"})
            except:
                tearDown()
                
                request.session.flush()
                if not request.session.exists(request.session.session_key):
                    request.session.create()

                cache.set('SESSION_KEY',request.session.session_key)

                session_id = request.session.session_key
                if request.POST['original'] and request.POST['short']:
                    cache.set(session_id, {'original':request.POST['original'], 'short':request.POST['short']})
                elif request.POST['original']:
                    cache.set(session_id, {'original':request.POST['original']})
                else:
                   messages.error(request, "Empty Fields")
                   return render(request, 'home.html')
                return render(request, 'signup.html')
        else:
            return render(request, 'signup.html')
    else:
        return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/login')