from rest_framework import routers
from django.urls import path, include
from user.views import *

urls = [
    path('user/health/', getAdminHealth),
    path('user/add/',addUser),
    path('user/login/',userLogin),

]