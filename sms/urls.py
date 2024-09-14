from django.urls import path
from .views import *
urlpatterns = [
    path('send_sms',send_sms),
    path('',home)
]