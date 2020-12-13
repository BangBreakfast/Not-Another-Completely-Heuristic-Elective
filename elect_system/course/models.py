from user.models import User
from django.db import models
import sys
import logging
sys.path.append("..")
'''
Course 类

属性:
    course_id: 主键
    name: 课程名称
    time: 上课时间
    info: 课程信息

外键:

'''


class Time(models.Model):
    day = models.IntegerField(default=1)
    period = models.IntegerField(default=1)


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)
    credit = models.IntegerField(blank=False)
    main_class = models.IntegerField(default=1)
    sub_class = models.CharField(max_length=32)
    lecturer = models.CharField(max_length=128)
    pos = models.CharField(max_length=128)
    dept = models.IntegerField(blank=False)
    detail = models.CharField(max_length=1024, null=True)

    capacity = models.IntegerField(default=50)
    elect_num = models.IntegerField(default=0)
    elect_newround_num = models.IntegerField(default=0)
    times = models.ManyToManyField(Time)

    def getCourseObj(crsId: str):
        crsSet = Course.objects.filter(course_id=crsId)
        if crsSet.count() != 1:
            logging.error('course set size error: courseId={}, size={}'.format(
                crsId, crsSet.count()))
            return None
        return crsSet.get()

    def isLegal(crsId: str) -> bool:
        return Course.objects.filter(course_id=crsId).exists()


# '''
# Elect 类

# 属性:
#     course: 所属于的课程
#     capacity: 课程容量
#     elect_num: 已经选上课的人数
#     elect_newround_num: 下一轮选课的人数


# 外键:

# '''


# class Elect(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     capacity = models.IntegerField(default=50)
#     elect_num = models.IntegerField(default=0)
#     elect_newround_num = models.IntegerField(default=0)


# '''
# Elected_stu 类

# 属性:
#     stu: 选课人
#     elect: 选课类
#     willpoint: 选课人投的意愿点数
#     elect_status: 选课状态 (等待抽签/选上了)

# '''


# class Elected_stu(models.Model):
#     stu = models.ForeignKey(User, on_delete=models.CASCADE)
#     elect = models.ForeignKey(Elect, on_delete=models.CASCADE)
#     willpoint = models.IntegerField()
#     status = [
#         ('1', 'Elect success!'),
#         ('2', 'Waiting ballot...'),
#     ]
#     elect_status = models.CharField(
#         max_length=2,
#         choices=status,
#         default='2',
#     )
