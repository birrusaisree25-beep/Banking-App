from .views import account_opening

from django.urls import path

urlpatterns = [
    path('savings/', account_opening,name= 'account_opening')
]