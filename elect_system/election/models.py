import logging
from django.db import models
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

    def getStudentOfCourse(crsId: str) -> list:
        stuSet = Election.objects.filter(courseId=crsId)
        return list(stuSet.all())

    def getCourseObj(crsId: str) -> Course:
        crsSet = Course.objects.filter(courseId=crsId)
        if crsSet.count() != 1:
            logging.error('course set size error: courseId={}, size={}'.format(
                crsId, crsSet.count()))
            return None
        return crsSet.get()

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
