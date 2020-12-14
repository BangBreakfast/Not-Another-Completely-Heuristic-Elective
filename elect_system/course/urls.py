from django.urls import path, re_path

from . import views

urlpatterns = [
    path('showallcourse', views.show_all_course),  # just for debug
	path('courses', views.course),
	re_path(r'courses/(\d{0,})', views.course),
	re_path(r'courses/(\d{0,})/detail', views.courseinfo),

]