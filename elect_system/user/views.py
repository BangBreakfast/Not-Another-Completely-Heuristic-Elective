from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import logging
import django.contrib.auth as auth
from .models import User, VerificationCode

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

    uid = reqData.get('uid')
    password = reqData.get('password')
    if uid is None or password is None:
        return None, None, 'Wrong parameters'
    return uid, password, None


@csrf_exempt
@DeprecationWarning
def register(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'msg': 'Wrong method'})
    uid, password, errMsg = FetchIdAndPasswd(request)
    if errMsg:
        return JsonResponse({'success': False, 'msg': errMsg})
    if User.objects.filter(username=uid).exists():
        return JsonResponse({'success': False, 'msg': 'uid already exist'})

    try:
        u = User.objects.create_user(username=uid, password=password)
        u.save()
    except:
        traceback.print_exc()
        return JsonResponse({'success': False, 'msg': 'Unknown error1'})

    return JsonResponse({'success': True})


@csrf_exempt
def login(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'msg': 'Wrong method'})
    uid, password, errMsg = FetchIdAndPasswd(request)
    if errMsg:
        return JsonResponse({'success': False, 'msg': errMsg})

    user = auth.authenticate(username=uid, password=password)
    if user is None:
        return JsonResponse({'success': False, 'msg': 'Authentication fails'})
    auth.login(request, user)
    return JsonResponse({'success': True})


@csrf_exempt
def logout(request: HttpRequest):
    if request.method == 'POST':
        auth.logout(request)
        return JsonResponse({
            'success': True,
        })
    else:
        return JsonResponse({
            "success": False,
            "msg": "Wrong method",
        })


@csrf_exempt
def test(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return JsonResponse({
                'success': True,
                'msg': 'This is a superuser!!!',
            })
        else:
            return JsonResponse({
                'success': True,
                'msg': 'A common user',
            })
    else:
        logger.warning('Unregistered user')
        return JsonResponse({
            'success': False,
            'msg': 'Please login first',
        })


@csrf_exempt
def changePasswd(request: HttpRequest):
    if request.method == 'GET':  # Get verification code to change passwd
        uid = request.GET.get('uid')
        if uid is None:
            return JsonResponse({'success': False, 'msg': 'Wrong param'})
        if not User.objects.filter(username=uid).exists():
            return JsonResponse({
                'success': False,
                'msg': 'uid does not exists'
            })

        uemail = uid + '@pku.edu.cn'  # uemail means 'user email'
        code = VerificationCode.getVerificationCode(uemail)
        send_mail('Verification code of PKU elective', str(code),
                  'pku_elective@163.com', [uemail])
        return JsonResponse({'success': True})
    elif request.method == 'POST':  # Verification code
        reqData = {}
        try:
            reqData = json.loads(request.body.decode())
        except:
            traceback.print_exc()
            return JsonResponse({'success': False, 'msg': 'Json format error'})
        passwd = reqData.get('password')
        uid = reqData.get('uid')
        vcode = reqData.get('vcode')
        if uid is None or passwd is None or vcode is None:
            return JsonResponse({'success': False, 'msg': 'Wrong param'})
        uemail = uid + '@pku.edu.cn'

        if not VerificationCode.objects.filter(email=uemail).exists():
            return JsonResponse({
                'success': False,
                'msg': 'uid does not exists'
            })
        v = VerificationCode.objects.get(email=uemail)
        if v.code != str(vcode):
            return JsonResponse({
                'success': False,
                'msg': 'Wrong verification code'
            })

        u = User.objects.get(username=uid)
        u.set_password(passwd)
        u.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'msg': 'Wrong method'})


# In fact, both student accounts and dean accounts could be accessed by this method
@csrf_exempt
def students(request: HttpRequest):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({'success': False, 'msg': 'User not authorized to this operation'})
    if request.method == 'POST':        # Create students
        try:
            reqData = json.loads(request.body.decode())
        except:
            traceback.print_exc()
            return JsonResponse({'success': False, 'msg': 'Json format error'})

        stus = reqData.get('students')
        if not isinstance(stus, list):
            return JsonResponse({'success': False, 'msg': 'Param type error'})
        for stu in stus:
            stuId = stu.get('stuId')
            stuName = stu.get('name')
            stuIsMale = stu.get('gender')
            stuDept = stu.get('dept')
            stuGrade = stu.get('grade')
            stuPasswd = stu.get('password')
            if not isinstance(stuId, str) or \
               not isinstance(stuName, str) or \
               not isinstance(stuIsMale, bool) or \
               not isinstance(stuDept, int) or \
               not isinstance(stuGrade, int) or \
               not isinstance(stuPasswd, str):
                return JsonResponse({'success': False, 'msg': 'Param type error'})
            if stuId is None or stuPasswd is None:
                return JsonResponse({'success': False, 'msg': 'Wrong param'})
            if User.objects.filter(username=stuId).exists():    # User already exists
                return JsonResponse({'success': False, 'msg': 'User already exists'})
            try:
                u = User.objects.create_user(
                    username=stuId, name=stuName, isMale=stuIsMale,
                    dept=stuDept, grade=stuGrade, password=stuPasswd,
                )
                u.save()
            except:
                traceback.print_exc()
                return JsonResponse({'success': False, 'msg': 'Unknown error1'})
            return JsonResponse({'success': True})
    elif request.method == 'GET':
        # TODO: search by fields combinations
        uid = request.GET.get('uid')
        user = User.objects.get(username=uid)
        userDict = {
            'stuId': user.username,
            'name': user.name,
            'isMale': user.isMale,
            'dept': user.dept,
            'grade': user.grade,
        }
        return JsonResponse({'success': True, 'data': userDict})
    elif request.method == 'PUT':
        # TODO: edit student info
        pass
    elif request.method == 'DELETE':
        # No check here. It's ok to delete an invalid uid.
        uid = request.GET.get('uid')
        userSet = User.objects.filter(username=uid)
        userSet.delete()
        return JsonResponse({'success': True})
