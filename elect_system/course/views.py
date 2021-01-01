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

#展示所有课程的函数，要求请求格式为POST，且处于用户登陆的状态
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

#对于课程时间格式的验证函数，用来判断课程的时间段是否正确
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

#将当前学生所选course列表中的课程时间进行统计汇总
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

#检验学生选课后是否发生时间冲突的函数
def check_time(course, day, period):
    times = course.times.all()
    for time in times:
        if time.day == day and (time.period in period):
            return True
    return False


@csrf_exempt
def course(request: HttpRequest, crsIdInURL: str = ''):
    # 添加新的课程（可以是一个新课程的列表），要求添加请求为POST，并检查操作权限
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
            #对欲添加课程时间的格式进行检查
            if not isinstance(times, list):
                logging.error('Course time format err, times={}'.format(times))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
            
            if not check_time_format(times):
                logging.error('Course time format err, times={}'.format(times))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

            # 如果当前想要添加的课程id已经在列表中存在（实际上也就是不支持课号一样的课程，与北大选课网有所区别）
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
    #通过GET请求来获取满足查询条件的课程列表
    elif request.method == 'GET':
        # 这里如果在request结构体中没有填写课程的某些属性作为查询条件，则返回空字符串
        crsId = request.GET.get('id')
        dept = request.GET.get('dept')
        period = request.GET.get('period')
        day = request.GET.get('day')
        name = request.GET.get('name')
        main_class = request.GET.get('main_class')
        sub_class = request.GET.get('sub_class')

        if crsIdInURL != '':
            crsId = crsIdInURL
        #依照搜寻条件依次进行层次查询
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

    # 编辑课程的相关信息，采用PUT的请求方式
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

        # NOTE: 只支持一次修改一个课程的相关信息
        #       同时进行多个课程的修改会报错
        if len(crss) > 1:
            logging.error(ERR_TYPE.GT_ONE)
            return JsonResponse({'success': False, 'msg': ERR_TYPE.GT_ONE})

        # 此处并不是一个真正的循环，实际上在crss的list中只有一个crs元素
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

            # 想要修改的课程如果不存在，则进行一个报错
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

    # 用DELETE类型的请求来删除一个课程
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

#查看课程详细信息的函数（主要用于前端交互功能：点击选课列表中已选课程来查看该课程的详细信息）
@csrf_exempt
def courseDetail(request: HttpRequest, course_id: str = ''):
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
                "capacity": course.capacity,
            }
            return JsonResponse(course_json)
        except:
            return JsonResponse({'success': False, 'msg': ERR_TYPE.COURSE_404})
    else:
        JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})
