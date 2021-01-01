from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import logging
import time
import django.contrib.auth as auth
from .models import User, VerificationCode, stuLock, Message
from elect_system.settings import ERR_TYPE
from threading import Lock
from datetime import datetime

logger = logging.getLogger(__name__)


def init():
    userSet = User.objects.all()
    for u in userSet:
        stuLock[u.username] = Lock()


init()

#返回关于选课的JsonResponse：coming soon
@csrf_exempt
def comingSoon(request: HttpRequest):
    response = {
        'msg': 'coming soon...',
    }
    return JsonResponse(response)

#从http请求中获取uid以及password
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

#注册函数，要求请求类型为Post，先检查是否已经有同uid的用户存在，否则，创建该用户
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

#登录函数，要求请求类型为Post，使用验证模块进行登陆验证，验证成功后完成用户登录
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

#注销函数，同样要求请求格式为Post
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

#权限检测函数，用来判断当前用户为教务还是学生
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

#修改密码函数，用验证码的方式来完成密码的修改
@csrf_exempt
def password(request: HttpRequest, uid: str = ''):
    # 获取验证码来进行密码的修改，请求方式为GET
    if request.method == 'GET':
        if uid is None:
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

        uSet = User.objects.filter(username=uid)
        if not uSet.exists():
            logging.error(
                'User changing passwd does not exist: {}'.format(uid))
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.AUTH_FAIL,
            })

        if uSet.count() > 1:
            logging.error('Duplicate username: {}'.format(uid))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.UNKNOWN})

        u = uSet.get()

        uemail = uid + '@pku.edu.cn'  # uemail means 'user email'
        code = VerificationCode.getVerificationCode(u)
        title = 'PKU elective verification code'
        content = 'Hello ' + uid + ', your verification code: ' + str(code)
        officialEmail = 'pku_elective@163.com'
        send_mail(title, content, officialEmail, [uemail])
        return JsonResponse({'success': True})

    # 使用验证码来完成密码的修改，请求方式为POST
    elif request.method == 'POST':
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

        vSet = VerificationCode.objects.filter(user__username=uid)
        if not vSet.exists():
            logging.error(
                'User changing passwd doesn\'t have vcode: {}'.format(uid))
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.AUTH_FAIL,
            })

        v = vSet.get()

        # 验证码错误
        if v.code != str(vcode):
            logging.error(
                'User changing passwd with wrong vcode: uid={}, got_vcode={}'.format(uid, vcode))
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.AUTH_FAIL,
            })

        v.user.set_password(passwd)
        v.user.save()
        v.delete()
        return JsonResponse({'success': True})

    else:
        logging.error(ERR_TYPE.INVALID_METHOD)
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})


# NOTE: 事实上，学生帐户和教务帐户都可以通过这种方法访问
@csrf_exempt
def students(request: HttpRequest, uid: str = ''):
    # 同时创建多个用户
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
            stuCreditLimit = stu.get('credit_limit')

            try:
                if stuDept:
                    stuDept = int(stuDept)
                if stuGrade:
                    stuGrade = int(stuGrade)
                if stuGender:
                    stuGender = bool(stuGender)
                else:
                    stuGender = True
                if stuCreditLimit:
                    stuCreditLimit = int(stuCreditLimit)
                else:
                    stuCreditLimit = 25
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
                    creditLimit=stuCreditLimit
                )
                u.save()
                stuLock[u.username] = Lock()
            except:
                traceback.print_exc()
                logging.error("Unknown error 15213")
                return JsonResponse({'success': False, 'msg': ERR_TYPE.UNKNOWN})

        return JsonResponse({'success': True})

    # Retrive user info
    # 学生不能够查看其他学生的个人信息，教务可以获取学生的信息列表
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
                'curWillingpoint': user.curWp    # This field is not used
            }
            userList.append(userDict)
        return JsonResponse({'success': True, 'data': userList})

    # 编辑学生的个人信息，使用PUT的方式来传递参数（需要处理对不同信息的编辑处理请求）
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

    # 删除一个用户
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

#发送信息函数
@csrf_exempt
def message(request: HttpRequest, mid=''):
    logging.debug(request.user.username)
    if not request.user.is_authenticated:
        logging.error('Anonymous user cannot get messages')
        return JsonResponse({
            'success': False,
            'msg': ERR_TYPE.NOT_ALLOWED,
        })

    # 将发送的信息标注为已经阅读
    if request.method == 'POST':
        # For dean, just return success
        if request.user.is_superuser:
            return JsonResponse({'success': True})

        if mid == 'all':
            u = User.objects.filter(username=request.user.username).get()
            userMsgSet = u.messages.all()
            for msg in userMsgSet:
                msg.hasRead = True
                msg.save()
        else:
            try:
                mid = int(mid)
            except:
                traceback.print_exc()
                logging.error(
                    'Read msg param error, id={}'.format(mid))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

            msgSet = Message.objects.filter(id=mid)
            if not msgSet.exists():
                logging.error('Read a nonexistent message, id={}'.format(mid))
                return JsonResponse({'success': False, 'msg': ERR_TYPE.MSG_404})
            msg = msgSet.get()
            msg.hasRead = True
            msg.save()
        return JsonResponse({'success': True})

    # 获取消息列表
    elif request.method == 'GET':
        # Note：由于教务和学生不是同一类用户，为了简化工作这里实际上没有为教务设计消息列表
        if request.user.is_superuser:
            return JsonResponse({'success': True, 'messages': []})

        uSet = User.objects.filter(username=request.user.username)
        u = uSet.get()
        msgList = []
        userMsgSet = u.messages.all()
        unReadCnt = 0
        for msg in userMsgSet:
            msgDict = {
                'id': msg.id,
                'time': int(msg.genTime.timestamp())*1000,
                'title': msg.title,
                'content': msg.content,
                'hasRead': msg.hasRead
            }
            msgList.append(msgDict)
            if not msg.hasRead:
                unReadCnt += 1
        return JsonResponse({'success': True, 'unReadNum': unReadCnt, 'messages': msgList})

    else:
        logging.error(ERR_TYPE.INVALID_METHOD)
        return JsonResponse({'success': False, 'msg': ERR_TYPE.INVALID_METHOD})
