from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import logging
import django.contrib.auth as auth
from .models import User, VerificationCode
from elect_system.settings import ERR_TYPE

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
        logging.error('Json format error, req.body={}'.format(
            request.body.decode()))
        return None, None, ERR_TYPE.JSON_ERR

    uid = reqData.get('uid')
    password = reqData.get('password')
    if uid is None or password is None:
        logging.error('Login without params')
        return None, None, ERR_TYPE.PARAM_ERR
    return uid, password, None


@csrf_exempt
@DeprecationWarning
def register(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})
    uid, password, errMsg = FetchIdAndPasswd(request)
    if errMsg:
        return JsonResponse({'success': False, 'msg': errMsg})
    if User.objects.filter(username=uid).exists():
        return JsonResponse({'success': False, 'msg': ERR_TYPE.USER_DUP})

    try:
        u = User.objects.create_user(username=uid, password=password)
        u.save()
    except:
        traceback.print_exc()
        return JsonResponse({'success': False, 'msg': ERR_TYPE.UNKNOWN})

    return JsonResponse({'success': True})


@csrf_exempt
def login(request: HttpRequest):
    if request.method != 'POST':
        logging.warn('Invalid method({})'.format(request.method))
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})

    try:
        reqData = json.loads(request.body.decode())
    except:
        traceback.print_exc()
        logging.error('Json format error, req.body={}'.format(
            request.body.decode()))
        return JsonResponse({'success': False, 'msg': ERR_TYPE.JSON_ERR})

    uid = reqData.get('uid')
    password = reqData.get('password')
    if uid is None or password is None:
        logging.error('Login without params')
        return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

    user = auth.authenticate(username=uid, password=password)
    if user is None:
        logging.warn('Login fail, uid={}'.format(uid))
        return JsonResponse({'success': False, 'msg': ERR_TYPE.AUTH_FAIL})
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
            "msg": ERR_TYPE.INVALID_METHOD,
        })


@csrf_exempt
def test(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return JsonResponse({
                'success': True,
                'msg': 'This is a superuser, uid={}'.format(request.user.username),
            })
        else:
            return JsonResponse({
                'success': True,
                'msg': 'A common user, uid={}'.format(request.user.username),
            })
    else:
        logger.warning('Unregistered user')
        return JsonResponse({
            'success': False,
            'msg': 'Please login first',
        })


@csrf_exempt
def password(request: HttpRequest, uid: str = ''):
    if request.method == 'GET':  # Get verification code to change passwd
        if uid is None:
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
        if not User.objects.filter(username=uid).exists():
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.AUTH_FAIL,
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
            return JsonResponse({'success': False, 'msg': ERR_TYPE.JSON_ERR})
        passwd = reqData.get('password')
        uid = reqData.get('uid')
        vcode = reqData.get('vcode')
        if uid is None or passwd is None or vcode is None:
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
        uemail = uid + '@pku.edu.cn'

        if not VerificationCode.objects.filter(email=uemail).exists():
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.AUTH_FAIL,
            })
        v = VerificationCode.objects.get(email=uemail)
        if v.code != str(vcode):
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.AUTH_FAIL,
            })
        VerificationCode.objects.filter(email=uemail).delete()
        u = User.objects.get(username=uid)
        u.set_password(passwd)
        u.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})


# NOTE: In fact, both student accounts and dean accounts could be accessed by this method
@csrf_exempt
def students(request: HttpRequest, uid: str = ''):
    # Multiple users are created at a time
    # TODO: For one illegal user info, just skip it and process other users
    if request.method == 'POST':
        if not request.user.is_authenticated or not request.user.is_superuser:
            logging.warn('Unprivileged user try to create user, uid={}'.format(
                request.user.username))
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.NOT_ALLOWED,
            })
        try:
            reqData = json.loads(request.body.decode())
        except:
            traceback.print_exc()
            logging.error('Json format error, req.body={}'.format(
                request.body.decode()))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.JSON_ERR})
        stus = reqData.get('students')
        if not isinstance(stus, list):
            logging.error('no students list')
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

        for stu in stus:
            uid = stu.get('uid')
            stuName = stu.get('name')
            stuGender = stu.get('gender')
            stuDept = stu.get('dept')
            stuGrade = stu.get('grade')
            stuPasswd = stu.get('password')

            try:
                if stuDept:
                    stuDept = int(stuDept)
                if stuGrade:
                    stuGrade = int(stuGrade)
                if stuGender:
                    stuGender = bool(stuGender)
            except:
                traceback.print_exc()
                logging.warn('Param type error, type(stuDept)={}, type(stuGrade)={}, type(stuGender)={}'.format(
                    type(stuDept), type(stuGrade), type(stuGender)))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

            if uid is None or stuPasswd is None:
                logging.warn('Missing uid or passwd')
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
            if User.objects.filter(username=uid).exists():    # User already exists
                logging.warn('User uid={} already exists'.format(uid))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.USER_DUP})
            try:
                u = User.objects.create_user(
                    username=uid, name=stuName, gender=stuGender,
                    dept=stuDept, grade=stuGrade, password=stuPasswd,
                )
                u.save()
            except:
                traceback.print_exc()
                logging.error("Unknown error 15213")
                return JsonResponse({'success': False, 'msg': ERR_TYPE.UNKNOWN})

        return JsonResponse({'success': True})

    # Retrive user info
    # Students cannot get user profile of others'
    elif request.method == 'GET':
        if not request.user.is_authenticated or \
                ((not request.user.is_superuser) and request.user.username != uid):
            logging.warn('Unprivileged user try to get user profile, uid={}'.format(
                request.user.username))
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.NOT_ALLOWED,
            })
        userSet = {}
        if uid == '':
            userSet = User.objects.filter()
        else:
            userSet = User.objects.filter(username=uid)
        if not userSet.exists():
            return JsonResponse({'success': True, 'data': []})
        userList = []
        for idx in range(0, userSet.count()):
            user = userSet[idx]
            userDict = {
                'uid': user.username,
                'name': user.name,
                'gender': user.gender,
                'dept': user.dept,
                'grade': user.grade,
                'creditLimit': user.creditLimit,
                'curCredit': user.curCredit,
                # 'willingpointLimit': user.willingpointLimit,
                'curWillingpoint':user.curWp    # This field is not used 
            }
            userList.append(userDict)
        return JsonResponse({'success': True, 'data': userList})

    # Edit user info
    elif request.method == 'PUT':
        if not request.user.is_authenticated or not request.user.is_superuser:
            logging.warn('Unprivileged user try to edit user profile, uid={}'.format(
                request.user.username))
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.NOT_ALLOWED,
            })
        if uid is '':
            logging.warn('Missing uid')
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
        userSet = User.objects.filter(username=uid)
        if not userSet.exists():
            logging.warn('User uid={} to edit does not exist'.format(uid))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.USER_404})
        user = userSet.get()

        reqData = {}
        try:
            reqData = json.loads(request.body.decode())
        except:
            traceback.print_exc()
            logging.error('Json format error, req.body={}'.format(
                request.body.decode()))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.JSON_ERR})

        name = reqData.get('name')
        dept = reqData.get('dept')
        gender = reqData.get('gender')
        grade = reqData.get('grade')
        creditLimit = reqData.get('credit_limit')
        passwd = reqData.get('password')

        try:
            if name:
                name = str(name)
            if creditLimit:
                creditLimit = int(creditLimit)
            if grade:
                grade = int(grade)
            if dept:
                dept = int(dept)
            if gender:
                gender = bool(gender)
            if passwd:
                passwd = str(passwd)
        except:
            traceback.print_exc()
            logging.warn('Edit user param type error')
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

        if name:
            user.name = name
        if dept:
            user.dept = dept
        if gender:
            user.gender = gender
        if grade:
            user.grade = grade
        if creditLimit:
            user.creditLimit = creditLimit
        if password:
            user.set_password(passwd)
        user.save()
        return JsonResponse({'success': True})

    # Delete a user
    elif request.method == 'DELETE':
        if not request.user.is_authenticated or not request.user.is_superuser:
            logging.warn('Unprivileged user try to delete user, uid={}'.format(
                request.user.username))
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.NOT_ALLOWED,
            })
        # No check here. It's ok to delete an invalid uid.
        userSet = User.objects.filter(username=uid)
        userSet.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})
