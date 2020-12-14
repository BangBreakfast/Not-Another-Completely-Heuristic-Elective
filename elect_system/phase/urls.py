from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
	path('phases', views.phases),
	re_path(r'phases/(\d){0,}', views.phases),
	path('current', views.current),
]
