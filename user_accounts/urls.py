from user_accounts.views import signup,login_user,verify_otp

from django.urls import path

urlpatterns = [
    path('signup/', signup, name= 'signup'), #endpoint,function names,identifier
    path('signin/', login_user, name= 'signin'),
    path('otp/', verify_otp, name='otp')
    
]
