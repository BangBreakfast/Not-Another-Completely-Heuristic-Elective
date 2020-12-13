from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
	re_path(r'schedule/(\w){0,}', views.schedule),
	path('elect', views.elect)
]
