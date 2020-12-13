import logging
from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Sum
from user.models import User
from course.models import Course
from elect_system.settings import ELE_TYPE
# Create your models here.


class Election(models.Model):
    stuId = models.IntegerField(blank=False)
    courseId = models.IntegerField(blank=False)
    willpoint = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    def getCourseOfStudent(stuId: str) -> list:
        if User.objects.filter(stuId=stuId):
            logging.error(
                'stuId={} does not exist in Course list'.format(stuId))
            return 0, 0
        crSet = Election.objects.filter(stuId=stuId)
        return list(crSet.all())

    def getWpCnt(stuId: str) -> int:
        if User.objects.filter(stuId=stuId):
            logging.error(
                'stuId={} does not exist in Course list'.format(stuId))
            return 0, 0
        q0 = Q()
        q0.connector = 'OR'
        q0.children.append(('status', ELE_TYPE.ELECTED))
        q0.children.append(('status', ELE_TYPE.PENDING))
        crsSet = Election.objects.filter(stuId=stuId)
        crsSet = crsSet.filter(q0)
        total = crsSet.all().aggregate(tatal=Sum('willpoint'))
        return total.get('total')

    def getStudentOfCourse(crsId: str) -> list:
        stuSet = Election.objects.filter(courseId=crsId)
        return list(stuSet.all())

    # Should check if this courseId is legal
    def getCourseElecionNum(crsId: str) -> list:
        crSet = Election.objects.filter(courseId=crsId)
        if Course.objects.filter(courseId=crsId):
            logging.error(
                'courseId={} does not exist in Course list'.format(crsId))
            return 0, 0
        elected = crSet.filter(status=ELE_TYPE.ELECTED).count()
        pending = crSet.filter(status=ELE_TYPE.PENDING).count()
        return elected, pending
