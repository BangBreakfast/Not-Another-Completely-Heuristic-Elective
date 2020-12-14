from django.test import TestCase
from user.models import User
from elect_system.settings import ERR_TYPE
import json


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
            "start_time": 1601012345000,
            "end_time": 1701012345000,
        }
        p1 = {
            "theme": "ballot1",
            "is_open": False,
            "detail": "Nothing here...",
            "start_time": 1701012345000,
            "end_time": 1801012345000,
        }
        respData = self.client.post(
            '/phase/phases', json.dumps({'phases': [p0, p1]}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        respData = self.client.get('/phase/phases')
        resp = respData.json()
        self.assertEqual(len(resp.get('data')), 2)
        phaseId = resp.get('data')[0].get('id')

        # Dean delete a phase
        respData = self.client.delete('/phase/phases/' + str(phaseId))
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        respData = self.client.get('/phase/phases')
        resp = respData.json()
        self.assertEqual(len(resp.get('data')), 1)

        # Dean logout
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
