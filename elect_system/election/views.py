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
from elect_system.settings import ELE_TYPE, ERR_TYPE


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
        crs = Course.getCourseObj(courseId)
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
            logging.error('Duplicate election: stu={}, crs={}, count={}'.format(
                request.user.username, courseId, elSet.count()))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_DUP})

        wpCnt = Election.getWpCnt(request.user.username)
        if wpCnt + wp > request.user.willingpointLimit:
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_FAIL})
        # TODO: credit check
        el = Election(willingpoint=wp, courseId=courseId,
                      stuId=request.user.username)
        el.save()

    # Edit wp
    elif typeId == 1:
        if elSet.count() != 0:
            logging.error('Duplicate election: stu={}, crs={}, count={}'.format(
                request.user.username, courseId, elSet.count()))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_DUP})
        el = elSet.get()

        wpCnt = Election.getWpCnt(request.user.username)
        if wpCnt - el.willingpoint + wp > request.user.willingpointLimit:
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_FAIL})
        el.willingpoint = wp
        el.save()

    # Quit pending
    elif typeId == 2:
        if elSet.count() != 1:
            logging.error('This election does not exists: stu={}, crs={}'.format(
                request.user.username, courseId))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_404})
        el = elSet.get()
        if el.status != ELE_TYPE.PENDING:
            logging.error('This election does not support this operation: stu={}, crs={}, op={}'.format(
                request.user.username, courseId, typeId))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_FAIL})
        el.delete()

    # Drop
    elif typeId == 3:
        if elSet.count() != 1:
            logging.error('This election does not exists: stu={}, crs={}'.format(
                request.user.username, courseId))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_404})
        el = elSet.get()
        if el.status != ELE_TYPE.ELECTED:
            logging.error('This election does not support this operation: stu={}, crs={}, op={}'.format(
                request.user.username, courseId, typeId))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_FAIL})
        el.delete()
