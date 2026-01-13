from django.shortcuts import render,redirect
from user_accounts.models import UserAccounts, EmailOtp
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login 
from django.contrib import messages
import random

# Create your views here.

def signup(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("psw")
        confirm_password = request.POST.get("psw-repeat")
        print(fname,lname,email,password,confirm_password)

        if password != confirm_password:
            return render(request,'user_accounts/signup.html',{
                "error":"Password and Confirm password do not match"
            })

        if UserAccounts.objects.filter(email=email).exists():
            return render(request,'user_accounts/signup.html',{
                "error":"User with this email already exists"
            })


        UserAccounts.objects.create(
            first_name = fname,
            last_name = lname,
            email = email,
            password = password,

        )

        send_mail(
            subject = "Welcome to My Bank",
            message= f"Hi {fname}, welcome to my bank. your username setup is successfull",
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list= {email}
        )
        return render(request,'user_accounts/signin.html')
    return render(request,'user_accounts/signup.html')

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserAccounts.objects.get(email=email)
            request.session["user_name"] = user.first_name
            if user.password == password:
                otp = str(random.randint(100000,999999))
                EmailOtp.objects.create(email=email,otp=otp)

                send_mail(
                    subject = "Login Code",
                    message= f"Hi {request.session["user_name"]} , Login code for My Bank app is \n {otp}",
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    recipient_list= {email}
                )       
                request.session["otp_email"] = user.email
                messages.success(request,"otp sent successfully")
                return redirect('otp')
        except UserAccounts.DoesNotExist:
            messages.error(request, "User does not exist")

    return render(request, "user_accounts/signin.html")

def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        print(otp)
        email = request.session.get("otp_email")
        print(email)
        try:
            res = EmailOtp.objects.filter(
                email=email,
                otp = otp,
                is_verified=False
            ).latest("created_at")

            if res.is_expired():
                messages.error(request,"otp timedout")
                return redirect('signin')
            res.is_verified = True
            res.save()

            user = UserAccounts.objects.get(email=email)
            print("validated user")
            request.session["user_name"] = user.first_name            
            request.session["user_email"] = user.email
            messages.success(request,"login successfull")
            return redirect("/")
        except EmailOtp.Exception:
            messages.error(request, "invalid otp")
    return render(request, "user_accounts/otp.html")
        
