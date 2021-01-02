from django.urls import path
from django.urls import re_path

from . import views
#election类的urlpath设置
urlpatterns = [
	path('schedule', views.schedule),
	re_path(r'schedule/(\w{0,})', views.schedule),
	path('elect', views.elect)
]
