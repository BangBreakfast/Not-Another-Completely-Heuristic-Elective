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
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
# from election.views import fairBallot

# sch = BackgroundScheduler()
# sch.add_jobstore(DjangoJobStore(), 'default')

# # TODO
# phaseTheme = {}

# @csrf_exempt
# def phases_new(request: HttpRequest, phid: str = ''):
#     if request.method == 'POST':
#         startBallot = sch.add_job(fairBallot, trigger='date', run_date=...)    # Begin ballot
#         endBallot = sch.add_job(fairBallot, trigger='date', run_date=...)    # End of ballot???
#         phaseTheme[startBallot.id] = '...'
#         phaseTheme[endBallot.id] = '...'
#     elif request.method == 'GET':
#         jobs = sch.get_jobs()
#         for j in jobs:
#             phaseTheme.get(j.id)
#         return []

def curPhase() -> Phase:
    now = timezone.now()
    ph = None
    phaseSet = Phase.objects.filter(startTime__lte=now)
    phaseSet = phaseSet.filter(endTime__gt=now)
    if phaseSet.count() == 0:
        # logging.warn('Not in any phases now')
        return None
    elif phaseSet.count() > 1:
        logging.error('Overlapping phases! count={}'.format(phaseSet.count()))
        return None
    else:
        ph = phaseSet.get()
    return ph


def isOpenNow() -> bool:
    cp = curPhase()
    if cp is None:  # TODO: Default should be false?
        return True
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
        if not request.user.is_authenticated or not request.user.is_superuser:
            logging.warn('Unprivileged user try to create phase, uid={}'.format(
                request.user.username))
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.NOT_ALLOWED,
            })

        try:
            reqData = json.loads(request.body.decode())
        except:
            traceback.print_exc()
            logging.error('Json format error, req.body={}'.format(
                request.body.decode()))
            return JsonResponse({'success': False, 'msg': ERR_TYPE.JSON_ERR})

        phs = reqData.get('phases')
        if not phs:
            logging.error('Create phase without phs')
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})
        if not isinstance(phs, list):
            logging.error('phs is not list')
            return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

        phSet = Phase.objects.filter()

        # NOTE: the front end only support adding one phase per request,
        #       warn on multiple additions
        if len(phs) > 1:
            logging.error(ERR_TYPE.GT_ONE)
            return JsonResponse({'success': False, 'msg': ERR_TYPE.GT_ONE})

        # Only on element in list. Not a real loop
        for ph in phs:
            phTheme = ph.get('theme')
            phDetail = ph.get('detail')
            if phDetail is None:
                phDetail = ''
            phIsOpen = ph.get('is_open')
            phStartTime = ph.get('start_time')
            phEndTime = ph.get('end_time')

            try:
                phTheme = str(phTheme)
                phDetail = str(phDetail)
                phIsOpen = bool(phIsOpen)
                phStartTime = int(phStartTime)
                phEndTime = int(phEndTime)
            except:
                traceback.print_exc()
                logging.warn('Create phase param type error')
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

            if phTheme is None or phIsOpen is None or \
                    phStartTime is None or phEndTime is None:
                logging.warn('Missing required params')
                return JsonResponse({'success': False, 'msg': ERR_TYPE.PARAM_ERR})

            # Make system aware of current timezone (Copy from CSDN)
            startDateTime = timezone.make_aware(datetime.fromtimestamp(
                phStartTime/1000), timezone.get_current_timezone())
            endDateTime = timezone.make_aware(datetime.fromtimestamp(
                phEndTime/1000), timezone.get_current_timezone())

            p = Phase(theme=phTheme, isOpen=phIsOpen,  detail=phDetail,
                      startTime=startDateTime, endTime=endDateTime)
            for ph in phSet:
                if p.overlapWith(ph):
                    logging.error(ERR_TYPE.OVERLAP)
                    return JsonResponse({'success':False, 'msg':ERR_TYPE.OVERLAP})
            if p.inThisPhase():
                logging.error(ERR_TYPE.HOT_EDIT)
                return JsonResponse({'success': False, 'msg': ERR_TYPE.HOT_EDIT})
                
            p.save()
        return JsonResponse({'success': True})

    elif request.method == 'DELETE':
        if not request.user.is_authenticated or not request.user.is_superuser:
            logging.warn('Unprivileged user try to delete phase, uid={}'.format(
                request.user.username))
            return JsonResponse({
                'success': False,
                'msg': ERR_TYPE.NOT_ALLOWED,
            })
        phSet = Phase.objects.filter(id=phid)
        for ph in phSet:
            if ph.inThisPhase():
                logging.error('Cannot delete current phase!(id={})'.format(ph.id))
                continue
            ph.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'msg': 'Invalid method'})
