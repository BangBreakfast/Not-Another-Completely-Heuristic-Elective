from django.db import models
from datetime import datetime
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler


# NOTE: This class is replaced by apscheduler and is no longer used.
class Phase(models.Model):
    startTime = models.DateTimeField(blank=False)
    endTime = models.DateTimeField(blank=False)
    theme = models.CharField(max_length=128, blank=False)
    # Is the elective system open or closed
    isOpen = models.BooleanField(blank=False)
    detail = models.CharField(max_length=1024, blank=True)

    def inThisPhase(self) -> bool:
        now = timezone.make_aware(datetime.now())
        return self.startTime < now and self.endTime > now

    def overlapWith(self, ph) -> bool:
        return not (self.startTime >= ph.endTime or self.endTime <= ph.startTime)

    # This method should be used only in unittest
    def fromDict(pdict: dict):
        return Phase(theme=pdict['theme'], isOpen=pdict["is_open"],  detail=pdict["detail"],
                     startTime=timezone.make_aware(datetime.fromtimestamp(
                         pdict["start_time"]/1000), timezone.get_current_timezone()),
                     endTime=timezone.make_aware(datetime.fromtimestamp(
                         pdict["end_time"]/1000), timezone.get_current_timezone()))


sch = BackgroundScheduler()
phaseTheme = {}
electionOpen = True
