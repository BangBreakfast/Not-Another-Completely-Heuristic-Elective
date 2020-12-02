from django.db import models
import django.contrib.auth.models

# Create your models here.

class Dean(django.contrib.auth.models.User):
	isMale = models.BooleanField(default=True)
	