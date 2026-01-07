from user_accounts.views import signup,signin,forgot_password

from django.urls import path

urlpatterns = [
    path('signup/', signup, name= 'signup'),
    path('signin/', signin, name= 'signin'),
    path('forgot-password/',forgot_password, name='forgot_password')
]
