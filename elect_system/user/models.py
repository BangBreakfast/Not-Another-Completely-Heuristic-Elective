from django.db import models
from django.utils import timezone
import django.contrib.auth.models
import random
from threading import Lock


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


class Message(models.Model):
    genTime = models.DateTimeField(null=False)
    title = models.CharField(max_length=256, null=False)
    content = models.CharField(max_length=8192, null=False) # Enough?
    hasRead = models.BooleanField(default=False, null=True)


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