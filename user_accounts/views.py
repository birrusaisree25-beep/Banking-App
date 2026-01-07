from django.shortcuts import render
from .models import UserAccounts
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def signup(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        #print(email)
        password = request.POST.get("psw")
        confirm_password = request.POST.get("psw-repeat")
        print(fname, lname, email,password,confirm_password)

        if password != confirm_password:
            return render(request,'user_accounts/signup.html', {
                "error":"Password and Confirm Password do not match"
            })
        
        if UserAccounts.objects.filter(email=email).exists():
               return render(request,'user_accounts/signup.html', {
                "error":"User with this email already exists"
            })
        
        UserAccounts.objects.create(
            first_name = fname,
            last_name = lname,
            email = email,
            password = password
         )


        send_mail(
             subject = "Welcome to my Bank",
             message = f"Hi {fname}, welcome to my bank. your username setup is successfull",
             from_email = settings.DEFAULT_FROM_EMAIL,
             recipient_list = {email}
            )

        return render(request,'user_accounts/signin.html')
    return render(request,'user_accounts/signup.html')

def signin(request):
    message = None
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("psw")
        print(username,password)

        
        try:
            user = UserAccounts.objects.get(email=username, password=password)

            # ✅ Success message
            message = f"Hey Login successful! Welcome back."
            print("Login successful")

        except UserAccounts.DoesNotExist:
            message = f"Invalid email or password"
            print(" login failed")

    return render(request,'user_accounts/signin.html', {
        'message':message
    })

def forgot_password(request):
    message="" 

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = UserAccounts.objects.get(email=email)
            send_mail(
                subject = 'Password Reset Request',
                message = 'Click this link to reset your password: http://127.0.0.1:8000/user_accounts/reset-password/',
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list = {email},
                fail_silently=False,
                # settings.EMAIL_HOST_USER,
            )
            message = "Password reset link sent to your email."

        except UserAccounts.DoesNotExist:
            message = "Email not found."

    return render(request, 'user_accounts/forgot_password.html',{
        'message':message
    })    
          
          
         