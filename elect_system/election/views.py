from django.http.request import HttpRequest
from django.http.response import JsonResponse
from .models import Election
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import traceback
from django.utils import timezone
import logging
from elect_system.settings import ERR_TYPE


@csrf_exempt
def schedule(request: HttpRequest, uid: str = ''):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})
    if not request.user.is_authenticated or \
            ((not request.user.is_superuser) and request.user.username != uid):
        return JsonResponse({
            'success': False,
            'msg': ERR_TYPE.NOT_ALLOWED,
        })
    elSet = Election.objects.filter(stu=uid)


@csrf_exempt
def elect(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})
    if not request.user.is_authenticated or request.user.is_superuser:
        return JsonResponse({
            'success': False,
            'msg': ERR_TYPE.NOT_ALLOWED,
        })
    try:
        reqData = json.loads(request.body.decode())
    except:
        traceback.print_exc()
        return JsonResponse({'success': False, 'msg': ERR_TYPE.JSON_ERR})
    typeId = reqData.get('type')
    courseId = reqData.get('course_id')
    wp = reqData.get('willingpoint')
    if typeId == 0:
        el = Election(willingpoint=wp)
