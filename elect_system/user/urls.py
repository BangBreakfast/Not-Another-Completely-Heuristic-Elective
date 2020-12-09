from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    # path('register', views.register),	# Do not use this method in production environment
    path('login', views.login),
    path('logout', views.logout),
    path('chpasswd', views.changePasswd),
    path('test', views.test),
    path('students', views.students)	# Only deans can perform
]
