import typing
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from .models import Election
from user.models import User
from course.models import Course
from phase.models import Phase
from course.views import get_time_json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import time
import traceback
from django.utils import timezone
import logging
from elect_system.settings import ELE_TYPE, ERR_TYPE
import random


@csrf_exempt
def schedule(request: HttpRequest, uid: str = ''):
    if request.method == 'GET':
        if uid == '':
            uid = request.user.username
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
                "course_id": crs.course_id,
                "name": crs.name,
                "credit": crs.credit,
                "main_class": crs.main_class,
                "sub_class": crs.sub_class,
                "times": get_time_json(crs),
                "lecturer": crs.lecturer,
                "pos": crs.pos,
                "dept": crs.dept,
                "election": {
                    "status": el.status,
                    "willingpoint": el.willingpoint,
                    "elected_num": electedNum,
                    "capacity": crs.capacity,
                    "pending_num": pendingNum
                }
            }
            crsList.append(crDict)
        return JsonResponse({'success': True, 'data': crsList})

    else:
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})


def checkTime(stuId: str, crsId: str) -> bool:
    crs = Course.getCourseObj(crsId)

    times = crs.times.all()
    tt = [[0 for i in range(10)] for j in range(8)]
    for time in times:
        d = time.day
        p = time.period
        tt[d][p] = 1

    # All courses that are elected or pending
    epList = Election.getCourseOfStudent(stuId)
    for ce in epList:
        crsId_ = ce.courseId
        c = Course.getCourseObj(crsId_)
        for time in c.times.all():
            d = time.day
            p = time.period
            if tt[d][p]:
                return False
    return True


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
    if wp is None:
        wp = 0
    elif wp < 0:
        return JsonResponse({'success': False, 'msg': ERR_TYPE.WP_ERR})
    elSet = Election.objects.filter(
        stuId=request.user.username, courseId=courseId)

    if typeId == 0:
        if elSet.count() != 0:
            logging.error('Duplicate election: stu={}, crs={}, count={}'.format(
                request.user.username, courseId, elSet.count()))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_DUP})
        if not Course.isLegal(courseId):
            return JsonResponse({'success': False, 'msg': ERR_TYPE.COURSE_404})

        wpCnt = Election.getWpCnt(request.user.username)
        if wpCnt + wp > 99:
            return JsonResponse({'success': False, 'msg': ERR_TYPE.WP_ERR})
        if not checkTime(request.user.username, courseId):
            return JsonResponse({'success': False, 'msg': ERR_TYPE.TIME_CONF})
        # TODO: credit check

        el = Election(willingpoint=wp, courseId=courseId,
                      stuId=request.user.username, status=ELE_TYPE.PENDING)
        el.save()
        return JsonResponse({'success': True})

    # Edit wp
    elif typeId == 1:
        if elSet.count() != 1:
            logging.error('This election does not exists: stu={}, crs={}'.format(
                request.user.username, courseId))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_DUP})
        el = elSet.get()

        wpCnt = Election.getWpCnt(request.user.username)
        if wpCnt - el.willingpoint + wp > 99:
            return JsonResponse({'success': False, 'msg': ERR_TYPE.WP_ERR})
        el.willingpoint = wp
        el.save()
        return JsonResponse({'success': True})

    # Quit pending
    elif typeId == 2:
        if elSet.count() != 1:
            logging.error('This election does not exists: '
                          'stu={}, crs={}'.format(request.user.username,
                                                  courseId))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_404})
        el = elSet.get()
        if el.status != ELE_TYPE.PENDING:
            logging.error('This election does not support this operation: '
                          'stu={}, crs={}, op={}'.format(request.user.username,
                                                         courseId, typeId))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_FAIL})
        el.delete()
        return JsonResponse({'success': True})

    # Drop
    elif typeId == 3:
        if elSet.count() != 1:
            logging.error('This election does not exists: stu={}, crs={}'.format(
                request.user.username, courseId))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_404})
        el = elSet.get()
        if el.status != ELE_TYPE.ELECTED:
            logging.error('This election does not support this operation: '
                          'stu={}, crs={}, op={}'.format(request.user.username,
                                                         courseId, typeId))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.ELE_FAIL})
        el.delete()
        return JsonResponse({'success': True})

    else:
        return JsonResponse({"success": False, 'msg': ERR_TYPE.PARAM_ERR})


def random_select(wpList, num):
    base_wp = 10
    wpList = [x + base_wp for x in wpList]
    for o in range(num):
        k = random.randint(1, sum(wpList))
        s = 0
        for i, x in enumerate(wpList):
            if s < k and s + x >= k:
                wpList[i] = 0
                break
            s += x
    return [i for i, x in enumerate(wpList) if x == 0]


def random_elect():
    '''
    TODO support this api
    '''
    crsList = Course.objects.all()
    for crs in crsList:
        elList = Election.objects.filter(courseId=crs.course_id)
        capacity = crs.elect_num
        elect_num = elList.filter(status=ELE_TYPE.ELECTED)
        pending_num = elList.filter(status=ELE_TYPE.PENDING)
        if elect_num + pending_num <= capacity:
            for el in elList:
                if el.status == ELE_TYPE.PENDING:
                    el.status = ELE_TYPE.ELECTED
                    el.save()
        else:
            elList = elList.filter(status=ELE_TYPE.PENDING)
            wpList = [el.willingpoint for el in elList]
            elected_stu = random_select(wpList, capacity - elect_num)
            index = 0
            for i, el in enumerate(elList):
                if index >= len(elected_stu):
                    el.delete()
                elif i == elected_stu[index]:
                    el.status = ELE_TYPE.ELECTED
                    el.save()
                    index += 1
                else:
                    el.delete()
    return True


# Watcher thread:
def runWatcher():
    while True:
        time.sleep(60)
        electionHasStarted = False
        if not Phase.isOpen() and not electionHasStarted:
            random_elect()
            electionHasStarted = True
        else:
            electionHasStarted = False

