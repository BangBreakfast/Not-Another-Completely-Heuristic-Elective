from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.http import response
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import django.contrib.auth as auth
from course.models import Course, Time
from elect_system.settings import ERR_TYPE


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

def check_time_format(time):
    ''' TODO
    [
        {"day":2, "period":[3,4]},
        {"day":4, "period":[5,6]},
    ]
    '''
    return True

# TODO: Crud of course
# NOTE: In fact, both student accounts and dean accounts could be accessed by this method
@csrf_exempt
def course(request: HttpRequest, uid: str = ''):
    # TODO: time PARAM CHECK

    if request.method == 'POST':
        if not request.user.is_authenticated or not request.user.is_superuser:
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.NOT_ALLOWED,
            })

        try:
            reqDatas = json.loads(request.body.decode())
        except:
            traceback.print_exc()
            return JsonResponse({'success': False, 'msg': ERR_TYPE.JSON_ERR})
        for reqData in reqDatas.values():

            course_id = reqData.get('course_id')
            name = reqData.get('name')
            credit = reqData.get('credit')
            lecturer = reqData.get('lecturer')
            pos = reqData.get('pos')
            dept = reqData.get('dept')
            detail = reqData.get('detail')

            times = reqData.get('times')
            election = reqData.get('election')
            print('start check format ...')
            ''' 
            print(isinstance(name, str))
            print(isinstance(credit, int))
            print(isinstance(lecturer, str))
            print(isinstance(pos, str))
            print(isinstance(dept, int))
            print(isinstance(times, list))
            print(isinstance(election, dict))
            print(election)
            '''

            if not isinstance(course_id, int) or \
                    not isinstance(name, str) or \
                    not isinstance(credit, int) or \
                    not isinstance(lecturer, str) or \
                    not isinstance(pos, str) or \
                    not isinstance(dept, int) or \
                    not isinstance(detail, str) or \
                    not isinstance(times, list) or \
                    not isinstance(election, dict):
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
            print('first check pass')

            elected_num = election.get('elected_num')
            capacity = election.get('capacity')
            pending_num = election.get('pending_num')
            if not isinstance(elected_num, int) or \
                    not isinstance(capacity, int) or \
                    not isinstance(pending_num, int) or \
                    not check_time_format(times):
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
            #TODO: time PARAM CHECK

            if Course.objects.filter(course_id=course_id).exists():  # course already exists
                return JsonResponse({'success': False, 'msg': ERR_TYPE.COURSE_DUP})

            try:
                c = Course.objects.create(course_id=course_id,
                                          name=name,
                                          credit=credit,
                                          lecturer=lecturer,
                                          pos=pos,
                                          dept=dept,
                                          detail=detail,
                                          elect_num=elected_num,
                                          capacity=capacity,
                                          elect_newround_num=pending_num)
                c.save()
            except:
                traceback.print_exc()
                return JsonResponse({'success': False, 'msg': ERR_TYPE.UNKNOWN})
            for tim in times:
                day = tim.get('day')
                period = tim.get('period')
                if not isinstance(day, int) or \
                        not isinstance(period, list) :
                    return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
                for per in period:
                    try:
                        t = Time.objects.create(course=c, day=day, period=per)
                        t.save()
                    except:
                        traceback.print_exc()
                        return JsonResponse({'success': False, 'msg': ERR_TYPE.UNKNOWN})

            return JsonResponse({'success': True})
    else :
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})