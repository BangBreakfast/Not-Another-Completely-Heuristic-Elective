from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.http import response
from django.views.decorators.csrf import csrf_exempt
import json, traceback
import django.contrib.auth as auth
# Create your views here.
from course.models import Course, Elect


@csrf_exempt
def show_all_course(request: HttpRequest):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, 'msg': 'Please login first', })
	if request.method != 'POST':
		return JsonResponse({'success': False, 'msg': 'Wrong method', })

	courseList = Course.objects.all()
	courseinfo_list = []
	for course in courseList:
		elect = Elect.objects.get(course=course)
		couserInfo = {
			"name": course.name,
			"time": course.time,
			"info": course.info,
			"capacity": elect.capacity,
			"elected": elect.elect_num,
			"waiting_num": elect.elect_newround_num
		}
		courseinfo_list.append(couserInfo)

	return JsonResponse({'success': True, 'msg': courseinfo_list, })
