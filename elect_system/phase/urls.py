from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
	# path('phases', views.phases),
	# re_path(r'phases/(\d){0,}', views.phases),
	path('phases', views.phases_new),
	re_path(r'phases/(\d){0,}', views.phases_new),
	# path('current', views.current),
]
