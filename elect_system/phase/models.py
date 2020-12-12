from django.db import models
from datetime import datetime

# Create your models here.


class Phase(models.Model):
    startTime = models.DateTimeField(blank=False)
    endTime = models.DateTimeField(blank=False)
    theme = models.CharField(max_length=128, blank=False)
    # Is the elective system open or closed
    isOpen = models.BooleanField(blank=False)
    detail = models.CharField(max_length=1024, blank=True)

    def inThisPhase(self) -> bool:
        now = datetime.now()
        return self.startTime < now and self.endTime > now
