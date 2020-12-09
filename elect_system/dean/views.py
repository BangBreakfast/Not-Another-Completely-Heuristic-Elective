from django.http import HttpResponse, JsonResponse, HttpRequest
from django.http import response
from django.views.decorators.csrf import csrf_exempt
import json, traceback
import django.contrib.auth as auth
from .models import Dean
from course.models import Course
from course.models import Elect

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.http import response
from django.views.decorators.csrf import csrf_exempt
import json, traceback
import django.contrib.auth as auth
# Create your views here.
from course.models import Course, Elect


def check_add_course_format(reqData):
	'''
	Json 格式检查，形式如下面这样
	{
	   "course_name":{
			"name": string,   // 课程名称
			"time": string,   // 上课时间
			"info": string,   // 课程简单介绍
			"capacity": int   //课程最大容量
    	}
    }
    格式正确返回 True 错误返回 False
	'''
	#TODO
	return True

@csrf_exempt
def addCourse(request: HttpRequest):
	if not request.user.is_authenticated:
		return JsonResponse({'success': False, 'msg': 'Please login first', })
	if request.method != 'POST':
		return JsonResponse({'success':False, 'msg':'Wrong method'})

	try:
		reqData = json.loads(request.body.decode())
	except:
		traceback.print_exc()
		return JsonResponse({'success':False, 'msg':'json load failed'})

	if not check_add_course_format(reqData):   #TODO
		return JsonResponse({'success':False, 'msg':'Json format Wrong'})

	for name, info in reqData.items():
		course = Course()
		course.name = info['name']
		course.time = info['time']
		course.info = info['info']

		elect = Elect()
		elect.course = course
		elect.capacity = info['capacity']

		try:
			course.save()
			elect.save()
		except:
			response = {
				"success": False,
				"msg": 'save failed'
			}
			return JsonResponse(response)


	return JsonResponse({'success': True, 'msg': 'Add course success!', })



@csrf_exempt
def comingSoon(request: HttpRequest):
	response = {
		'msg': 'coming soon...',
	}
	return JsonResponse(response)

def FetchIdAndPasswd(request: HttpRequest):
	reqData = {}
	try:
		reqData = json.loads(request.body.decode())
	except:
		traceback.print_exc()
		return None, None, 'Json format error'

	if 'deanId' not in reqData.keys() or 'password' not in reqData.keys():
		return None, None, 'Wrong parameters'
	deanId = reqData['deanId']
	password = reqData['password']
	if not (deanId and password):
		return None, None, 'Wrong parameters'
	return deanId, password, None

@csrf_exempt
def register(request: HttpRequest):
	if request.method != 'POST':
		return JsonResponse({'success':False, 'msg':'Wrong method'})
	deanId, password, errMsg = FetchIdAndPasswd(request)
	if errMsg:
		return JsonResponse({'success':False, 'msg':errMsg})
	if Dean.objects.filter(username=deanId).exists():
		return JsonResponse({'success':False, 'msg':'deanId already exist'})
	
	try:
		dean = Dean.objects.create_user(username=deanId, password=password)
		dean.save()
	except:
		traceback.print_exc()
		return JsonResponse({'success':False, 'msg':'Unknown error1'})

	return JsonResponse({'success':True, 'msg':'Create dean success'})

@csrf_exempt
def login(request: HttpRequest):
	if request.method != 'POST':
		return JsonResponse({'success':False, 'msg':'Wrong method'})
	deanId, password, errMsg = FetchIdAndPasswd(request)
	if errMsg:
		return JsonResponse({'success':False, 'msg':errMsg})

	user = auth.authenticate(username=deanId, password=password)
	if user is None:
		return JsonResponse({'success':False, 'msg':'Authentication fails'})
	auth.login(request, user)
	return JsonResponse({'success':True, 'msg':'Dean successfully login'})

@csrf_exempt
def logout(request: HttpRequest):
	if request.method == 'POST':
		auth.logout(request)
		return JsonResponse({'success': True, 'msg':'Dean successfully logout'})
	else:
		return JsonResponse({
			"success": False,
			"msg": "Wrong method",
		})

@csrf_exempt
def test(request: HttpRequest):
	if request.user.is_authenticated:
		return JsonResponse({'success': True, 'msg':'This is an authenticated dean',})
	else:
		return JsonResponse({'success': False, 'msg':'Please login first',})

@csrf_exempt
def createStu(request: HttpRequest):
	response = {
		'code': 1,
		'data': {
			'msg': 2,
		},
	}
	return JsonResponse(response)

