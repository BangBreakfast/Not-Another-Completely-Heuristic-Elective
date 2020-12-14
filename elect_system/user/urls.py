from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    # path('register', views.register),	# Do not use this method in production environment
    path('login', views.login),
    path('logout', views.logout),
    path('password', views.password),
    re_path(r'password/(\d{0,})', views.password),
    path('students', views.students),
    re_path(r'students/(\d{0,})', views.students),
    path('test', views.test),
]
