import typing
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from .models import Election
from course.models import Course
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

    elList = Election.getCourseOfStudent(stuId=uid)
    crsList = []
    for el in elList:
        courseId = el.courseId
        crs = Election.getCourseObj(courseId)
        if crs is None:
            continue
        electedNum, pendingNum = Election.getCourseElecionNum(courseId)
        crDict = {
            "course_id": crs.courseId,
            "name": crs.name,
            "credit": crs.credit,
            "times": crs.time,
            "lecturer": crs.lecturer,
            "pos": crs.pos,
            "dept": crs.dept,
            "election": {
                "status": el.status,
                "willpoint": el.willpoint,
                "elected_num": electedNum,
                "capacity": crs.capacity,
                "pending_num": pendingNum
            }
        }
        crsList.append(crDict)
    return JsonResponse({'success': True, 'data': crsList})


@csrf_exempt
# TODO: Not completed
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
    elSet = Election.objects.filter(
        stuId=request.user.username, courseId=courseId)
    if typeId == 0:
        if elSet.count() != 0:
            logging.error('exist')
            return JsonResponse({})
        el = Election(willingpoint=wp, courseId=courseId,
                      stuId=request.user.username)
        el.save()
    elif typeId == 1:
        elSet = Election.objects.filter(
            stuId=request.user.username, courseId=courseId)
        el = elSet.get()
        el.willingpoint = wp
        el.save()
    elif typeId == 2:
        pass
