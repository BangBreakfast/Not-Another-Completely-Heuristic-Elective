from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
	path('schedule', views.schedule),
	re_path(r'schedule/(\d{0,})', views.schedule),
	path('elect', views.elect)
]
