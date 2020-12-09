from django.db import models
from django.utils import timezone
import django.contrib.auth.models
import random

# Create your models here.


class VerificationCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    genTime = models.DateTimeField()

    def getVerificationCode(chMail: str):
        codeGen = 0
        if VerificationCode.objects.filter(email=chMail).exists():
            vc = VerificationCode.objects.get(email=chMail)
            if (timezone.now() - vc.genTime).total_seconds() < 30:
                return vc.code
            codeGen = random.randint(1000, 9999)
            vc.code = codeGen
            vc.genTime = timezone.now()
            vc.save()
        else:  # Does not exist
            codeGen = random.randint(1000, 9999)
            vc = VerificationCode(
                email=chMail, code=codeGen, genTime=timezone.now())
            vc.save()
        return codeGen


class User(django.contrib.auth.models.User):
    name = models.CharField(max_length=128)
    isMale = models.BooleanField(default=True)
    dept = models.CharField(max_length=128)
    grade = models.IntegerField()
    electedCourse = models.CharField(max_length=1024)

    def __str__(self) -> str:
        return '<' + self.username + ',' + str(self.isMale) + '>'
