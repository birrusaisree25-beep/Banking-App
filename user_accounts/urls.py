from user_accounts.views import signup,signin,forgot_password,reset_password,verify_otp

from django.urls import path

urlpatterns = [
    path('signup/', signup, name= 'signup'), #endpoint,function names,identifier
    path('signin/', signin, name= 'signin'),
    path('forgot-password/',forgot_password, name='forgot_password'),
    path('reset-password/',reset_password, name='reset_password'),
    path('otp/', verify_otp, name='otp')
    
]
