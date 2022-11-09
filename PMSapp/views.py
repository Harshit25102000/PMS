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
                   review_id = request.POST['review_id']
                   receiver_user = request.POST['receiver_user']
                   sender_user = request.POST['sender_user']
                   print(review_id,sender_user,receiver_user)

                   from datetime import timedelta

                   timezone=pytz.timezone('Asia/Kolkata')
                   now = datetime.datetime.now(tz=timezone)
                   dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                   print("date  =", dt_string[:10])
                   print("time =", dt_string[11:])
                   dates = dt_string[:10]
                   time = dt_string[11:]
                   manager_receiver= manager.objects.filter(user=User.objects.filter(email=receiver_user).first()).first()
                   employee_sender= employee.objects.filter(user=User.objects.filter(email=sender_user).first(
                   )).first()
                   review_instance= reviews.objects.filter(id=review_id).first()
                   comments.objects.create(review=review_instance,sender=User.objects.filter(email=sender_user).first(),
                   receiver=User.objects.filter(email=receiver_user).first(),
                   sender_name=employee_sender.First_name,receiver_name=manager_receiver.First_name,message=message,
                   date=dates,
                   time=time)

                   return redirect("commentspage",id=review_id)
              except Exception as e:
                   print(e)
                   messages.error(request,"comment was not made please contact the administrator")
                   return redirect("commentspage",id=review_id)
        else:
            return HttpResponse("404 not allowed")

    else:
        return HttpResponse("Please login")

def managerhome(request):
    pass

@login_required(login_url='/internlogin/')
def periodicreview(request):

    if request.user.is_employee:

        e = employee.objects.filter(user=request.user).first()
        if e is not None:



            review= reviews.objects.all().order_by('-id')

            context = {'reviews':review}
            return render(request,'periodicreview.html',context)
        return HttpResponse("You are not allowed to view this page. Make sure you are added in employee field")
    else:
        return HttpResponse("You are not allowed to view this Page")

@login_required(login_url='/internlogin/')
def commentspage(request,id):

    if request.user.is_employee:

        e = employee.objects.filter(user=request.user).first()
        if e is not None:



            comment= comments.objects.filter(review=id)

            review=reviews.objects.filter(id=id).first()

            review_user=review.user
            print(review_user)
            u=manager.objects.filter(user=review_user).first()
            print(e.First_name,u)


            context = {'comments':comment,'sender_user':request.user,'receiver_user':review_user,'review_id':id,
            'sender_name':e.First_name,'receiver_name':u.First_name,'review':review}
            print(context)
            return render(request,'comments.html',context)
        return HttpResponse("You are not allowed to view this page. Make sure you are added in employee field")
    else:
        return HttpResponse("You are not allowed to view this Page")

@login_required(login_url='/internlogin/')
def self_appraisal(request):

    if request.user.is_employee:

        e = employee.objects.filter(user=request.user).first()
        if e is not None:

            self_appraisal= self_appraisals.objects.filter(created_by=e).order_by('-id')
            context = {'self_appraisals': self_appraisal}


            return render(request,'self_appraisal.html',context)
        return HttpResponse("You are not allowed to view this page. Make sure you are added in employee field")
    else:
        return HttpResponse("You are not allowed to view this Page")


@login_required(login_url='/internlogin/')
def self_appraisalpage(request,id):

    if request.user.is_employee:

        e = employee.objects.filter(user=request.user).first()
        if e is not None:
            self_appraisal = self_appraisals.objects.filter(id=id).first()
            context = {'self_appraisal': self_appraisal}


            return render(request,'self_appraisalpage.html',context)
        return HttpResponse("You are not allowed to view this page. Make sure you are added in employee field")
    else:
        return HttpResponse("You are not allowed to view this Page")


@login_required(login_url='/internlogin/')
def self_appraisalform(request):
    if request.user.is_employee:

        e = employee.objects.filter(user=request.user).first()
        if e is not None:
            sending_by=e.First_name
            #sending_to =

            return render(request, 'self_appraisalform.html')
        return HttpResponse("You are not allowed to view this page. Make sure you are added in employee field")
    else:
        return HttpResponse("You are not allowed to view this Page")