from django.contrib import admin
from django.urls import path

import wega_auth
import calc
from home.views import Home
from wega_auth.views import RegisterUser

urlpatterns = [
    path('', Home.as_view(), name='home'),
 
]
