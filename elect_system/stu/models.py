from django.db import models
import django.contrib.auth.models

# Create your models here.

class Stu(django.contrib.auth.models.User):
	isMale = models.BooleanField(default=True)
	electedCourse = models.CharField(max_length=1024)