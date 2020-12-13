from django.urls import path

from . import views

urlpatterns = [
    path('showallcourse', views.show_all_course),  # just for debug
	path('course', views.course),
	path('courses', views.findcourse)
]