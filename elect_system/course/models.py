from django.db import models
from stu.models import Stu
'''
Course 类

属性:
    course_id: 主键
    name: 课程名称
    time: 上课时间
    info: 课程信息

外键:

'''
# Create your models here.
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=2000, null=True)
    time = models.CharField(max_length=2000, null=True)
    info = models.CharField(max_length=2000, null=True)



'''
Elect 类

属性:
    course: 所属于的课程
    capacity: 课程容量
    elect_num: 已经选上课的人数
    elect_newround_num: 下一轮选课的人数
        

外键:

'''
class Elect(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=50)
    elect_num = models.IntegerField(default=0)

    elect_newround_num = models.IntegerField(default=0)


'''
Elected_stu 类

属性:
    stu: 选课人
    elect: 选课类
    willpoint: 选课人投的意愿点数
    elect_status: 选课状态 (等待抽签/选上了)

'''

class Elected_stu(models.Model):
    stu = models.ForeignKey(Stu, on_delete=models.CASCADE)
    elect = models.ForeignKey(Elect, on_delete=models.CASCADE)
    willpoint = models.IntegerField()
    status = [
        ('1', 'Elect success!'),
        ('2', 'Waiting ballot...'),
    ]
    elect_status = models.CharField(
        max_length=2,
        choices=status,
        default='2',
    )


