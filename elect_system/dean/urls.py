from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('test', views.test),
	path('createStu', views.comingSoon),
    path('addcourse', views.addCourse),
]
