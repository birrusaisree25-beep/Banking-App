from django.shortcuts import render
from .models import User

# Create your views here.

def account_opening(request): 
    #Getting the date from UI when clicked on submit button
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        print(username,password,fname,lname,email,phone,role)

        if User.objects.filter(username=username).exists():
            return render(request,'users/account_opening.html',{'error':'username already exists'})
        
        #Writing this data into a User table
        user = User.objects.create_user(
            username = username,
            password = password,
            first_name = fname, 
            last_name = lname,
            email = email,
            phone = phone,
            role = role
        )
        
        
    return render(request, 'users/account_opening.html')