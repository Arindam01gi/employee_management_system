from rest_framework import routers
from django.urls import path, include
from user.views import *

urls = [
    path('user/health/', getAdminHealth),
    path('user/login/',userLogin),
    path('user/add/',addUser),
    path('user/view/',userView),
    path('user/list/',userList),
    path('user/delete/',userDelete),
    path('user/create_post/',createPost)
    

]