from django.urls import path, include

from . import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('test', views.test),
]
