from django.db import models
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json, traceback, logging
import django.contrib.auth as auth
from .models import Stu

logger = logging.getLogger(__name__)

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

	if 'stuId' not in reqData.keys() or 'password' not in reqData.keys():
		return None, None, 'Wrong parameters'
	stuId = reqData['stuId']
	password = reqData['password']
	if not (stuId and password):
		return None, None, 'Wrong parameters'
	return stuId, password, None

@csrf_exempt
def register(request: HttpRequest):
	if request.method != 'POST':
		return JsonResponse({'success':False, 'msg':'Wrong method'})
	stuId, password, errMsg = FetchIdAndPasswd(request)
	if errMsg:
		return JsonResponse({'success':False, 'msg':errMsg})
	if Stu.objects.filter(username=stuId).exists():
		return JsonResponse({'success':False, 'msg':'stuId already exist'})
	
	try:
		stu = Stu.objects.create_user(username=stuId, password=password)
		stu.save()
	except:
		traceback.print_exc()
		return JsonResponse({'success':False, 'msg':'Unknown error1'})

	return JsonResponse({'success':True, 'msg':'Create stu success'})

@csrf_exempt
def login(request: HttpRequest):
	if request.method != 'POST':
		return JsonResponse({'success':False, 'msg':'Wrong method'})
	stuId, password, errMsg = FetchIdAndPasswd(request)
	if errMsg:
		return JsonResponse({'success':False, 'msg':errMsg})

	user = auth.authenticate(username=stuId, password=password)
	if user is None:
		return JsonResponse({'success':False, 'msg':'Authentication fails'})
	auth.login(request, user)
	return JsonResponse({'success':True, 'msg':'Stu successfully login'})

@csrf_exempt
def logout(request: HttpRequest):
	if request.method == 'POST':
		auth.logout(request)
		return JsonResponse({'success': True, 'msg':'Stu successfully logout'})
	else:
		return JsonResponse({
			"success": False,
			"msg": "Wrong method",
		})

@csrf_exempt
def test(request: HttpRequest):
	print(request.session.values())
	print(request.COOKIES)
	if request.user.is_authenticated:
		return JsonResponse({'success': True, 'msg':'This is an authenticated stu',})
	else:
		logger.warning('Unregistered user')
		return JsonResponse({'success': False, 'msg':'Please login first',})
