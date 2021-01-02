import logging
from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Sum
from user.models import User
from course.models import Course
from elect_system.settings import ELE_TYPE
import django.contrib.auth.models
'''
election类内容介绍
属性：
    stu：学生id（django user类本身的对外key）
    crs：课程id（在课程类下声明了其为课程的对外key）
    willingpoint：本次选课的意愿点
    credit：本次选课的学分
    status：选课的情况，分为None、Elected以及Pending
'''

class Election(models.Model):
    stu = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    crs = models.ForeignKey(Course, on_delete=models.PROTECT, null=False)
    willingpoint = models.IntegerField(default=0)
    credit = models.IntegerField(null=True)
    status = models.IntegerField(default=0)
    #获取学生的选课情况
    def getCourseOfStudent(stuId: str) -> list:
        crSet = Election.objects.filter(stu__username=stuId)
        return list(crSet.all())
    #计算该学生当前选课已经使用的意愿点数
    def getWpCnt(stuId: str) -> int:
        q0 = Q()
        q0.connector = 'OR'
        q0.children.append(('status', ELE_TYPE.ELECTED))
        q0.children.append(('status', ELE_TYPE.PENDING))
        crsSet = Election.objects.filter(stu__username=stuId)
        crsSet = crsSet.filter(q0)
        total = crsSet.all().aggregate(total=Sum('willingpoint'))
        tot = total.get('total')
        if tot is None:
            tot = 0
        return tot
    #获取选择了某一课程的全部学生的信息
    def getStudentOfCourse(crsId: str) -> list:
        stuSet = Election.objects.filter(crs=crsId)
        return list(stuSet.all())

    # 获取对于某一课程而言，当前已经选上课程的人数以及预计进行选课的人数
    def getCourseElecionNum(crsId: str):
        crSet = Election.objects.filter(crs=crsId)
        elected = crSet.filter(status=ELE_TYPE.ELECTED).count()
        pending = crSet.filter(status=ELE_TYPE.PENDING).count()
        return elected, pending
    #  检测函数，用于判断是否进行了重复选课
    def getStuElectionNum(stuId: str, crsId: str):
        elSet = Election.objects.filter(stu__username=stuId, crs=crsId)
        if elSet.count() == 1:
            return elSet.get().status, elSet.get().willingpoint
        elif elSet.count() > 1:
            logging.error(
                'Duplicate election: stuId={}, crsId={}'.format(stuId, crsId))
            return 0, 0
        else:
            return 0, 0
