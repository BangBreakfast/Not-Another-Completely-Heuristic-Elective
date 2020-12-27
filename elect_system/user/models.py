from django.db import models
from django.utils import timezone
import django.contrib.auth.models
import random
from threading import Lock



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

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    code = models.CharField(max_length=6)
    genTime = models.DateTimeField()

    def getVerificationCode(u: User):
        codeGen = 0
        vSet = VerificationCode.objects.filter(user=u.id)

        if vSet.exists():
            v = vSet.get()
            # Not allowed to get diff vcode within 30 seconds
            if (timezone.now() - v.genTime).total_seconds() < 30:
                return v.code
            codeGen = random.randint(1000, 9999)
            v.code = codeGen
            v.genTime = timezone.now()
            v.save()
        else:  # Does not exist
            codeGen = random.randint(1000, 9999)
            vc = VerificationCode.objects.create(
                user=u, code=codeGen, genTime=timezone.now())
            vc.save()
        return codeGen
