from django.contrib import admin
from django.urls import path

import wega_auth
import calc
from wega_auth.views import LoginUser, RegisterUser, LogoutUser

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),

 
 
]