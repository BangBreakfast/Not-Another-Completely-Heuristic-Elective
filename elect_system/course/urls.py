from django.urls import path, re_path

from . import views

urlpatterns = [
    path('showallcourse', views.show_all_course),  # just for debug
    path('courses', views.course),
    path('depts', views.dept),
    re_path(r'courses/(\d{0,})/detail', views.courseDetail),
    re_path(r'courses/(\d{0,})', views.course),

]
