from django.http.request import HttpRequest
from django.http.response import JsonResponse
from .models import Phase
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import traceback
from django.utils import timezone
import logging
from elect_system.settings import ERR_TYPE

# Create your views here.


def curPhase() -> Phase:
    now = timezone.now()
    ph = None
    phaseSet = Phase.objects.filter(startTime__lte=now)
    phaseSet = phaseSet.filter(endTime__gt=now)
    if phaseSet.count() != 1:
        # TODO: Internal error
        pass
    else:
        ph = phaseSet.get()
    return ph


def isOpenNow() -> bool:
    return curPhase().isOpen


@csrf_exempt
def current(request: HttpRequest):
    ph = curPhase()
    phDict = {
        'id': ph.id,
        'theme': ph.theme,
        'detail': ph.detail,
        'is_open': ph.isOpen,
        'start_time': ph.startTime,
        'end_time': ph.endTime,
    }
    return JsonResponse({'success': True, 'data': phDict})


@csrf_exempt
def phases(request: HttpRequest, phid: str = ''):
    if request.method == 'GET':
        phList = []
        phSet = Phase.objects.filter()
        for idx in range(0, phSet.count()):
            ph = phSet[idx]
            phDict = {
                'id': ph.id,
                'theme': ph.theme,
                'detail': ph.detail,
                'is_open': ph.isOpen,
                'start_time': ph.startTime,
                'end_time': ph.endTime,
            }
            phList.append(phDict)
        return JsonResponse({'success': True, 'data': phList})

    elif request.method == 'POST':
        try:
            reqData = json.loads(request.body.decode())
        except:
            traceback.print_exc()
            return JsonResponse({'success': False, 'msg': 'Json format error'})
        phs = reqData.get('phases')
        if not phs:
            return JsonResponse({'success': False, 'msg': 'Parameter type error'})
        if not isinstance(phs, list):
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
        for ph in phs:
            phTheme = ph.get('theme')
            phDetail = ph.get('detail')
            if phDetail is None:
                phDetail = ''
            phIsOpen = ph.get('is_open')
            phStartTime = ph.get('start_time')
            phEndTime = ph.get('end_time')
            if phTheme is None or phIsOpen is None or \
                phStartTime is None or phEndTime is None:
                return JsonResponse({'success':False, 'msg':ERR_TYPE.PARAM_ERR})
            if not isinstance(phTheme, str) or \
               not isinstance(phIsOpen, bool) or \
               not isinstance(phStartTime, int) or \
               not isinstance(phEndTime, int):
               return JsonResponse({'success':False, 'msg':ERR_TYPE.PARAM_ERR})
            
            startDateTime = timezone.make_aware(datetime.fromtimestamp(phStartTime/1000), timezone.get_current_timezone())
            endDateTime = timezone.make_aware(datetime.fromtimestamp(phEndTime/1000), timezone.get_current_timezone())
            p = Phase(theme=phTheme, isOpen=phIsOpen,  detail=phDetail,
                startTime=startDateTime, endTime=endDateTime)
            p.save()
        return JsonResponse({'success': True})
    elif request.method == 'DELETE':
        phSet = Phase.objects.filter(id=phid)
        phSet.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'msg': 'Invalid method'})
