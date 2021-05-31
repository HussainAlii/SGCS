import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from User.models import User
from worker.models import Worker
from command_center.models import CommandCenter


# sending variables with session
# request.session['username'] = username
# using session to display data
# {{ request.session.id }}

def signin(request):
    if request.method == 'POST':
        username = request.POST['username'].upper()
        # password = hash(request.POST['password'])
        password = request.POST['password'] #for testing only

        # to solve the national number problem .. check first index if c,w ok else send a message? it works but..
        if username[0] == 'E':
            if CommandCenter.objects.filter(username=username, password=password).exists():
                # here we add session data that we need for the CommandCenter
                request.session['username'] = username
                request.session['IsAdmin']  = isAdmin(username)
                return redirect("../command_center/")
            else:
                request.session.flush()
                messages.error(request, 'Invalid credentials')
                return redirect("/")
        elif username[0] == 'W':
            if Worker.objects.filter(username=username, password=password).exists():
                #here we add session data that we need for the Worker
                request.session['username'] = username
                return redirect( "../worker/")
            else:
                request.session.flush()
                messages.error(request, 'Invalid credentials')
                return redirect("/")
        else:
            try:
                if User.objects.filter(national_number=int(username), password=password).exists():
                    # here we add session data that we need for the User
                    request.session['username'] = username
                    request.session['points'] = User.objects.filter(national_number=username).values("points").first().get('points')
                    return redirect("../user/")
                else:
                    request.session.flush()
                    messages.error(request, 'Invalid credentials')
                    return redirect("/")
            except:
                request.session.flush()
                messages.error(request, 'Invalid credentials')
                return redirect("/")
    else:
        if 'username' not in request.session:
            pass
        else:
            if request.session['username'][0].upper() == 'E':
                if CommandCenter.objects.filter(username=request.session['username'].upper()).exists():
                    # here we add session data that we need for the CommandCenter
                    return redirect("../command_center/")
                else:
                    messages.error(request, 'Something went wrong')
                    return redirect("/")
            elif request.session['username'][0].upper() == 'W':
                if Worker.objects.filter(username=request.session['username'].upper()).exists():
                    # here we add session data that we need for the Worker
                    return redirect("../worker/")
                else:
                    messages.error(request, 'Something went wrong')
                    return redirect("/")
            elif User.objects.filter(national_number=request.session['username'].upper()).exists():
                # here we add session data that we need for the User
                return redirect("../user/")
            else:
                messages.error(request, 'Something went wrong')
                return redirect("/")
    
    if CommandCenter.objects.count()==0:
        CommandCenter(username='E1',password='E1',role='Admin',phone_number='0541738440',full_name='Admin',gender='Male',
                      country='Saudi Arabia',date_of_birth=datetime.date.today(),enrol_date=datetime.date.today(),isAdmin=True).save()

    return render(request, '../templates/static/signin.html',{'title': "Sign in"})

# Create your views here.

def forgetPassword(request):
    return render(request, 'static/forgot-password.html', {'title': "Forget Password"})


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['ConPassword']:
            if not User.objects.filter(national_number=request.POST['national_number']).exists():  # points
                # password = hash(request.POST['password'])
                password = request.POST['password']
                User(national_number=request.POST['national_number'], password=password).save()
                messages.success(request, 'you are successfully signed up')
                return redirect('/')
            else:
                messages.info(request, 'User already exists')
                return redirect('/')
        else:
            messages.error(request, 'Password and confirm password does not match')
            return redirect('../signup/')
    return render(request, '../templates/static/signup.html', {'title': "Sign up"})

def signout(request):
    request.session.flush()
    return redirect('/')

def resetPassword(request):
    return render(request, 'static/reset-password.html', {'title': "Reset Password"})

def isAdmin(username):
    empObj = CommandCenter.objects.filter(username=username).values('isAdmin').first()
    if empObj['isAdmin']:
        return 'true'
    return 'false'

