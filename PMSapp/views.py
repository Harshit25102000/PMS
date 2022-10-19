from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
import datetime
from django.contrib.auth import authenticate, login, logout
User = get_user_model()
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def internlogin(request):
    return render(request,'internlogin.html')

def internsignup(request):
    return render(request, 'internsignup.html')

def handle_employee_signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'passwords do not match')
            return redirect('internsignup')

        if '@' not in email:
            messages.error(request, 'Enter a valid email address')
            return redirect('internsignup')

        entry = entries.objects.filter(Email_id=email).first()
        if not entry:
            messages.error(request,'This email is not registered with organization')
            return redirect('internsignup')

        user = User.objects.filter(email=email).first()

        if user:
            messages.error(request, 'Account already exists with this Email ')
            return redirect('internsignup')

        siteuser = User.objects.create_user(email, password1)
        siteuser.save()

        employee_id=entry.employee_id
        first_name=entry.First_name
        #if entry.Middle_name is None:
            #middle_name = ''

        middle_name=entry.Middle_name
        last_name=entry.Last_name
        dept= entry.Department
        desig=entry.Designation
        email=entry.Email_id
        phone=entry.phone
        joining_date=entry.joining_date
        reporting_manager=entry.Reporting_manager

        employeeuser = employee.objects.create(user=siteuser,
        employee_id=employee_id,
        First_name=first_name,
        Middle_name=middle_name,
        Last_name=last_name,
        Department=dept,
        Designation=desig,
        Email_id=email,
        phone=phone,
        joining_date=joining_date,
        Reporting_manager=reporting_manager,

        )
        employeeuser.save()
        messages.success(request, "Account created successfully")
        return redirect('employeehome')


        #except Exception as e:

        #    print(e)
        #    messages.error(request, "e")
        #    return redirect('internsignup')





    else:
        return HttpResponse('404 Not Allowed')


def handle_employee_login(request):
    if request.method == 'POST':
        email= request.POST['email']
        password = request.POST['password']

        if '@' not in email:
            messages.error(request, 'Enter a valid email address')
            return redirect('internlogin')
        
        user = authenticate(email=email, password=password)

        if user is not None:
            if not user.is_employee:
                messages.error(request, 'Please login using employee credentials')
                return redirect('internlogin')
            login(request, user)
            messages.success(request,"Account logged in successfully")
            print(request.user)
            return redirect('employeehome')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('internlogin')
    else:
        return HttpResponse('404 not allowed')

def logout_view(request):
    logout(request)
    messages.success(request, 'User logged Out successfully')
    return redirect('internlogin')

@login_required(login_url='/internlogin/')
def employeehome(request):


    if request.user.is_employee:

        e = employee.objects.filter(user=request.user).first()
        if e is not None:

            progress=e.progress

            comment= comments.objects.all().order_by('-id')

            context = {'user':e,'progress':progress,'comments':comment}
            return render(request,'employeehome.html',context)
        return HttpResponse("You are not allowed to view this page. Make sure you are added in employee field")
    else:
        return HttpResponse("You are not allowed to view this Page")

@login_required(login_url='/internlogin/')
def employee_profile(request):
    if request.user.is_employee:
        e = employee.objects.filter(user=request.user).first()
        if e is not None:
            context={'e':e}
            return render(request,'employeeprofile.html',context)
        return HttpResponse("You are not allowed to view this page. Make sure you are added in employee field")
    else:
        return HttpResponse("You are not allowed to view this Page")
import pytz
def make_comments(request):
    if request.user.is_authenticated:


        if request.method == 'POST':
              try:
                message = request.POST['message']
                from datetime import timedelta

                timezone=pytz.timezone('Asia/Kolkata')
                now = datetime.datetime.now(tz=timezone)
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                print("date  =", dt_string[:10])
                print("time =", dt_string[11:])
                dates = dt_string[:10]
                time = dt_string[11:]
                user = request.user
                if user.is_employee:
                    name=employee.objects.get(user=user).First_name
                elif user.is_manager:
                    name = manager.objects.get(user=user).First_name
                elif user.is_admin:
                    name = adminuser.objects.get(user=user).First_name
                else:
                    name= "Anonymous"
                comments.objects.create(user=request.user,name=name,message=message,date=dates,time=time)

                return redirect("employeehome")
              except Exception as e:
                   print(e)
                   messages.error(request,"comment was not made please contact the administrator")
                   return redirect("employeehome")
        else:
            return HttpResponse("404 not allowed")

    else:
        return HttpResponse("Please login")

def managerhome(request):
    pass