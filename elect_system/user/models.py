from django.db import models
from django.utils import timezone
import django.contrib.auth.models
import random
from threading import Lock

'''
类Mesaage用于传递信息
属性如下所示：
    genTime：消息发送时间
    title：消息标题
    content：消息文本内容
    hasRead：消息是否得到阅读
'''

class Message(models.Model):
    genTime = models.DateTimeField(null=False)
    title = models.CharField(max_length=256, null=False)
    content = models.CharField(max_length=8192, null=False) # Enough?
    hasRead = models.BooleanField(default=False, null=True)

'''
类User即为用户类
属性如下所示：
    name：用户的姓名
    gender：用户的性别（用boolean型表示，男性为true，女性为false）
    dept：用户所在的院系（默认为信息科学与技术学院）
    grade：用户所在的年级
    messages：消息列表，维护一个多对多的消息关系

    creditLimit：选课的学分限制(初始化为25学分)
    curCredit：当前已经选修的学分数量（初始化为0）
    willingpointLimit：意愿点的总数限制（初始化为99点意愿点）
    curWp：当前已经使用的意愿点数（初始化为0）
    isLegal：验证uid是否合法
    __str__：返回用户信息的字符串，用于后续的处理
'''
class User(django.contrib.auth.models.User):
    name = models.CharField(max_length=128)
    gender = models.BooleanField(default=True)  # male=True, female=False
    dept = models.IntegerField(default=48)
    grade = models.IntegerField(default=2017)
    messages = models.ManyToManyField(Message)

    creditLimit = models.IntegerField(default=25)
    curCredit = models.IntegerField(default=0)
    willingpointLimit = models.IntegerField(default=99)
    curWp = models.IntegerField(default=0)  # Not used

    def isLegal(uid: str) -> bool:
        return User.objects.filter(username=uid)

    def __str__(self) -> str:
        return '<' + self.username + ',' + str(self.gender) + ',' + \
            str(self.dept) + ',' + str(self.grade) + str(self.creditLimit) + \
            str(self.willingpointLimit) + '>'


stuLock = {}
'''
    VerificationCode类用于验证码的验证
    getVerificationCode：获取验证码（验证码内置cd：30秒）
'''
class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    code = models.CharField(max_length=6)
    genTime = models.DateTimeField()

    def getVerificationCode(u: User):
        codeGen = 0
        vSet = VerificationCode.objects.filter(user=u.id)

        if vSet.exists():
            v = vSet.get()
            # Not allowed to get diff vcode within 30 seconds
            if (timezone.now() - v.genTime).total_seconds() < 30:
                return v.code
            codeGen = random.randint(1000, 9999)
            v.code = codeGen
            v.genTime = timezone.now()
            v.save()
        else:  # Does not exist
            codeGen = random.randint(1000, 9999)
            vc = VerificationCode.objects.create(
                user=u, code=codeGen, genTime=timezone.now())
            vc.save()
        return codeGen
