from django.test import TestCase
from user.models import User
from phase.models import Phase
from elect_system.settings import ERR_TYPE
import json
from django.utils import timezone
from datetime import datetime


class PhaseTests(TestCase):
    def test_phases(self):
        u0 = User.objects.create_user('1600013239', password='123456')
        u0.save()

        u1 = User.objects.create_user('jyeecs', password='123456')
        u1.is_superuser = True
        u1.save()

        # Anonymous user not allowed to create or delete
        respData = self.client.post('/phase/phases')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        respData = self.client.delete('/phase/phases')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        # OK
        respData = self.client.get('/phase/phases')
        resp = respData.json()
        self.assertEqual(type(resp.get('data')), list)
        self.assertEqual(len(resp.get('data')), 0)

        # JY login
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1600013239', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        respData = self.client.get('/phase/phases')
        resp = respData.json()
        self.assertEqual(type(resp.get('data')), list)
        self.assertEqual(len(resp.get('data')), 0)

        respData = self.client.post('/phase/phases')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        # JY logout
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Dean login
        respData = self.client.post(
            '/user/login', json.dumps({'uid': 'jyeecs', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        respData = self.client.get('/phase/phases')
        resp = respData.json()
        self.assertEqual(type(resp.get('data')), list)
        self.assertEqual(len(resp.get('data')), 0)

        # Dean create a phase
        p0 = {
            "theme": "prepare1",
            "is_open": True,
            "detail": "Nothing here...",
            "start_time": 1400012345000,
            "end_time": 1500012345000,
        }
        p1 = {
            "theme": "ballot1",
            "is_open": False,
            "detail": "Nothing here...",
            "start_time": 1500012345000,
            "end_time": 1600012345000,
        }
        p2 = {
            "theme": "ballot2",
            "is_open": False,
            "detail": "Nothing here...",
            "start_time": 1450012345000,
            "end_time": 1550012345000,
        }
        p3 = {
            "theme": "ballot2",
            "is_open": False,
            "detail": "Nothing here...",
            "start_time": 1450012345000,
            "end_time": 1850012345000,
        }
        self.assertEqual(Phase.fromDict(p0).overlapWith(
            Phase.fromDict(p1)), False)
        self.assertEqual(Phase.fromDict(p0).overlapWith(
            Phase.fromDict(p2)), True)
        self.assertEqual(Phase.fromDict(p0).overlapWith(
            Phase.fromDict(p3)), True)

        self.assertEqual(Phase.fromDict(p0).inThisPhase(), False)
        self.assertEqual(Phase.fromDict(p3).inThisPhase(), True)

        respData = self.client.post(
            '/phase/phases', json.dumps({'phases': [p0, ]}), content_type="application/json")
        resp = respData.json()
        if resp.get('msg'):
            print('Error msg: ', resp.get('msg'))
        self.assertEqual(resp.get('success'), True)

        # Insert a overlap phase
        respData = self.client.post(
            '/phase/phases', json.dumps({'phases': [p2, ]}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.OVERLAP)

        respData = self.client.get('/phase/phases')
        resp = respData.json()
        self.assertEqual(len(resp.get('data')), 1)
        phaseId = resp.get('data')[0].get('id')

        # Dean delete a phase
        respData = self.client.delete('/phase/phases/' + str(phaseId))
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Insert a hot phase
        respData = self.client.post(
            '/phase/phases', json.dumps({'phases': [p3, ]}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.HOT_EDIT)

        respData = self.client.get('/phase/phases')
        resp = respData.json()
        self.assertEqual(len(resp.get('data')), 0)
