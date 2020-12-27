from election.models import Election
from course.models import DEPT
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.http import response
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import logging
import django.contrib.auth as auth
from course.models import Course, Time
from elect_system.settings import ERR_TYPE, ELE_TYPE
from django.db import IntegrityError

@csrf_exempt
def dept(request: HttpRequest):
    return JsonResponse({'success': True, 'data': DEPT})


@csrf_exempt
def show_all_course(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'msg': 'Please login first', })
    if request.method != 'POST':
        return JsonResponse({'success': False, 'msg': 'Wrong method', })
    courseList = Course.objects.all()
    courseinfo_list = []
    for course in courseList:
        couserInfo = {
            "name": course.name,
            "detail": course.detail,
            "capacity": course.capacity,
            "elected": course.elect_num,
            "waiting_num": course.elect_newround_num
        }
        courseinfo_list.append(couserInfo)

    return JsonResponse({'success': True, 'msg': courseinfo_list, })


def check_time_format(times: list):
    for t in times:
        if not isinstance(t, dict):
            return False
        day = t.get('day')
        if not isinstance(day, int) or day > 7 or day < 1:
            return False
        periods = t.get('period')
        if not isinstance(periods, list):
            return False
        for p in periods:
            if not isinstance(p, int) or p > 14 or p < 1:
                return False    
    return True


def get_time_json(course: Course):
    times = course.times.all()
    json = {}
    for time in times:
        day = time.day
        period = time.period
        if json.get(day):
            json[day]["period"].append(period)
        else:
            json[day] = {
                "day": day,
                "period": [period]
            }
    return [x for x in json.values()]


def check_time(course, day, period):
    times = course.times.all()
    for time in times:
        if time.day == day and (time.period in period):
            return True
    return False


@csrf_exempt
def course(request: HttpRequest, crsIdInURL: str = ''):
    # Add a new course
    if request.method == 'POST':
        if not request.user.is_superuser:
            logging.error('user create course without privilege')
            return JsonResponse({'success': False, 'msg': ERR_TYPE.NOT_ALLOWED})

        try:
            reqData = json.loads(request.body.decode())
        except:
            logging.error('Json format error, req.body={}'.format(
                request.body.decode()))
            traceback.print_exc()
            return JsonResponse({'success': False, 'msg': ERR_TYPE.JSON_ERR})

        crss = reqData.get('courses')
        if crss is None or type(crss) is not list:
            logging.error('courses param err, req={}'.format(reqData))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

        for crs in crss:
            courseId = crs.get('course_id')
            name = crs.get('name')
            credit = crs.get('credit')
            lecturer = crs.get('lecturer')
            pos = crs.get('pos')
            dept = crs.get('dept')

            name_eng = crs.get('name_eng')
            prerequisite = crs.get('prerequisite')
            detail = crs.get('detail')
            main_class = crs.get('main_class')
            sub_class = crs.get('sub_class')
            times = crs.get('times')
            capacity = crs.get('capacity')

            try:
                courseId = str(courseId)
                name = str(name)
                credit = int(credit)
                dept = int(dept)
                main_class = int(main_class)
                capacity = int(capacity)
            except:
                traceback.print_exc()
                logging.error(
                    'Create course param type error, crs={}'.format(crs))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

            if not isinstance(times, list):
                logging.error('Course time format err, times={}'.format(times))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
            
            if not check_time_format(times):
                logging.error('Course time format err, times={}'.format(times))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

            # course already exists
            if Course.objects.filter(course_id=courseId).exists():
                logging.error(
                    'Cannot add for course already exist, crsId={}'.format(courseId))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.COURSE_DUP})

            c = Course.objects.create(course_id=courseId, name=name, credit=credit,
                                      lecturer=lecturer, pos=pos, dept=dept,
                                      main_class=main_class, sub_class=sub_class,
                                      name_eng=name_eng, prerequisite=prerequisite,
                                      detail=detail, capacity=capacity)

            for tim in times:
                day = tim.get('day')
                periods = tim.get('period')
                if not isinstance(day, int) or \
                        not isinstance(periods, list):
                    logging.error(
                        'Time field error, error time={}'.format(times))
                    return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
                for period in periods:
                    tSet = Time.objects.filter(day=day, period=period)
                    try:
                        if tSet.exists():
                            t = tSet[0]
                            c.times.add(t)
                        else:
                            t = Time.objects.create(day=day, period=period)
                            t.save()
                            c.times.add(t)
                    except:
                        traceback.print_exc()
                        logging.error('Unknown err 8086')
                        return JsonResponse({'success': False, 'msg': ERR_TYPE.UNKNOWN})
            try:
                c.save()
            except:
                traceback.print_exc()
                logging.error('Unknown err 8087')
                return JsonResponse({'success': False, 'msg': ERR_TYPE.UNKNOWN})

        return JsonResponse({'success': True})

    elif request.method == 'GET':
        # For queries of args not carried in URL, empty string will be returned
        crsId = request.GET.get('id')
        dept = request.GET.get('dept')
        period = request.GET.get('period')
        day = request.GET.get('day')
        name = request.GET.get('name')
        main_class = request.GET.get('main_class')
        sub_class = request.GET.get('sub_class')

        if crsIdInURL != '':
            crsId = crsIdInURL

        course_list = Course.objects.all()
        if crsId:
            course_list = course_list.filter(course_id=crsId)
        if dept:
            course_list = course_list.filter(dept=dept)
        if name:
            course_list = course_list.filter(name=name)
        if main_class:
            course_list = course_list.filter(main_class=main_class)
        if sub_class:
            course_list = course_list.filter(sub_class=sub_class)
        if day and period:
            day = int(day)
            period = [int(x) for x in period.split(',')]
            course_list = [
                x for x in course_list if check_time(x, day, period)]

        course_json_list = []
        for course in course_list:
            elected, pending = Election.getCourseElecionNum(course.course_id)
            st, wp = 0, 0
            if request.user.is_authenticated:
                st, wp = Election.getStuElectionNum(
                    request.user.username, course.course_id)
            course_json = {
                "course_id": course.course_id,
                "name": course.name,
                "credit": course.credit,
                "main_class": course.main_class,
                "sub_class": course.sub_class,
                "times": get_time_json(course),
                "lecturer": course.lecturer,
                "pos": course.pos,
                "dept": course.dept,
                "election": {
                    "status": st,
                    "willingpoint": wp,
                    "elected_num": elected,
                    "capacity": course.capacity,
                    "pending_num": pending
                }
            }
            course_json_list.append(course_json)
        return JsonResponse({'success': True, 'course_list': course_json_list})

    # Edit course info
    elif request.method == 'PUT':
        if not request.user.is_superuser:
            logging.error('user edit course without privilege')
            return JsonResponse({'success': False, 'msg': ERR_TYPE.NOT_ALLOWED})

        try:
            reqData = json.loads(request.body.decode())
        except:
            logging.error('Json format error, req.body={}'.format(
                request.body.decode()))
            traceback.print_exc()
            return JsonResponse({'success': False, 'msg': ERR_TYPE.JSON_ERR})

        crss = reqData.get('courses')
        if crss is None or type(crss) is not list:
            logging.error('courses param err, req={}'.format(reqData))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

        # NOTE: only support edit one course per request,
        #       warn on multiple additions
        if len(crss) > 1:
            logging.error(ERR_TYPE.GT_ONE)
            return JsonResponse({'success': False, 'msg': ERR_TYPE.GT_ONE})

        # Only on element in list. Not a real loop
        for crs in crss:
            courseId = crs.get('course_id')
            name = crs.get('name')
            credit = crs.get('credit')
            lecturer = crs.get('lecturer')
            pos = crs.get('pos')
            dept = crs.get('dept')

            name_eng = crs.get('name_eng')
            prerequisite = crs.get('prerequisite')
            detail = crs.get('detail')
            main_class = crs.get('main_class')
            sub_class = crs.get('sub_class')
            times = crs.get('times')
            capacity = crs.get('capacity')

            try:
                courseId = str(courseId)
                if name:
                    name = str(name)
                if credit:
                    credit = int(credit)
                if dept:
                    dept = int(dept)
                if main_class:
                    main_class = int(main_class)
                if capacity:
                    capacity = int(capacity)
            except:
                traceback.print_exc()
                logging.error(
                    'Create course param type error, crs={}'.format(crs))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

            crsSet = Course.objects.filter(course_id=courseId)

            # course not exist
            if not crsSet.exists():
                logging.error(
                    'Cannot edit unexist course, crsId={}'.format(courseId))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.COURSE_404})
            c = crsSet.get()

            if name:
                c.name = name
            if credit:
                c.credit = credit
            if dept:
                c.dept = dept
            if main_class:
                c.main_class = main_class

            if capacity:
                if capacity >= c.capacity:
                    c.capacity = capacity
                else:
                    logging.warn(
                        'Cannot decrease course capacity, {}->{}'.format(c.capacity, capacity))
                    return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
            c.save()
        return JsonResponse({'success': True})

    # Delete a course
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            logging.error('user delete course without privilege')
            return JsonResponse({'success': False, 'msg': ERR_TYPE.NOT_ALLOWED})
        elSet = Election.objects.filter(crs=crsIdInURL)

        try:
            crsSet = Course.objects.filter(course_id=crsIdInURL)
            crsSet.delete()
        except IntegrityError:
            logging.error(
                'Cannot delete courses with students elected or pending, crsId={}'.format(crsIdInURL))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.HOT_EDIT})

        return JsonResponse({'success': True})

    else:
        logging.error('invalid method: {}'.format(request.method))
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})


@csrf_exempt
def courseinfo(request: HttpRequest, course_id: str = ''):
    if request.method == 'GET':
        try:
            course = Course.objects.get(course_id=course_id)

            def get_time_json(course):
                times = course.times.all()
                json = {}
                for time in times:
                    day = time.day
                    period = time.period
                    if json.get(day):
                        json[day]["period"].append(period)
                    else:
                        json[day] = {
                            "day": day,
                            "period": [period]
                        }
                return [x for x in json.values()]
            course_json = {
                "course_id": course.course_id,
                "name": course.name,
                "credit": course.credit,
                "main_class": course.main_class,
                "sub_class": course.sub_class,
                "times": get_time_json(course),
                "lecturer": course.lecturer,
                "pos": course.pos,
                "dept": course.dept,
                "name_eng": course.name_eng,
                "prerequisite": course.prerequisite,
                "detail": course.detail,
                "election": {
                    "status": 0,    # TODO: needed?
                    "willingpoint": 99,
                    "elected_num": course.elect_num,
                    "capacity": course.capacity,
                    "pending_num": course.elect_newround_num
                }
            }
            return JsonResponse(course_json)
        except:
            return JsonResponse({'success': False, 'msg': ERR_TYPE.COURSE_404})
    else:
        JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})
