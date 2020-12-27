import logging
from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Sum
from user.models import User
from course.models import Course
from elect_system.settings import ELE_TYPE
import django.contrib.auth.models


class Election(models.Model):
    stu = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    crs = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    willingpoint = models.IntegerField(default=0)
    credit = models.IntegerField(null=True)
    status = models.IntegerField(default=0)

    def getCourseOfStudent(stuId: str) -> list:
        crSet = Election.objects.filter(stu__username=stuId)
        return list(crSet.all())

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

    def getStudentOfCourse(crsId: str) -> list:
        stuSet = Election.objects.filter(crs=crsId)
        return list(stuSet.all())

    # Should check if this courseId is legal
    def getCourseElecionNum(crsId: str):
        crSet = Election.objects.filter(crs=crsId)
        elected = crSet.filter(status=ELE_TYPE.ELECTED).count()
        pending = crSet.filter(status=ELE_TYPE.PENDING).count()
        return elected, pending

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
