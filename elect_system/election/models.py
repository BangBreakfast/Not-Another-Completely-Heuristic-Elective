from django.db import models
from user.models import User
from course.models import Course
# Create your models here.


class Election(models.Model):
    stu = models.ForeignKey("User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    willpoint = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
