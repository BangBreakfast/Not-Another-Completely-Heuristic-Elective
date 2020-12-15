from django.http.response import JsonResponse
from django.test import TestCase
from .models import User
from elect_system.settings import ERR_TYPE
import json


class UserTests(TestCase):
    def test_login(self):
        u = User.objects.create_user('1500012345', password='123456')
        u.save()
        u = User.objects.create_user('1500054321', password='123456')
        u.save()

        # Invalid method
        respData = self.client.get('/user/login')
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.INVALID_METHOD)

        respData = self.client.put('/user/login')
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.INVALID_METHOD)

        respData = self.client.delete('/user/login')
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.INVALID_METHOD)

        # Parameter error
        respData = self.client.post(
            '/user/login', json.dumps({'password': '123456'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.PARAM_ERR)

        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500012345'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.PARAM_ERR)

        # Json format error
        # WARNING: Stack trace is printed on console when code reaches here
        respData = self.client.post(
            '/user/login', 'not_a_json_string', content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.JSON_ERR)

        # Wrong password
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500012345', 'password': 'zzz'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.AUTH_FAIL)

        # Id not exist
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500011111', 'password': '123456'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.AUTH_FAIL)

        # OK
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500012345', 'password': '123456'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Duplicated login should be allowed
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500012345', 'password': '123456'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Another account login
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500054321', 'password': '123456'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

    def test_logout(self):
        u = User.objects.create_user('1500012345', password='123456')
        u.save()

        # Invalid method
        respData = self.client.get('/user/logout')
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.INVALID_METHOD)

        respData = self.client.put('/user/logout')
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.INVALID_METHOD)

        respData = self.client.delete('/user/logout')
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.INVALID_METHOD)

        # OK
        respData = self.client.post('/user/logout')
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

    def test_password(self):
        u = User.objects.create_user('1600013239', password='123456')
        u.save()

        respData = self.client.get('/user/password/1600013239')
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

    def test_students(self):
        u = User.objects.create_user('jyeecs', password='123456')
        u.is_superuser = True
        u.save()

        # Anonymous user is not allowed to get student profile
        respData = self.client.get('/user/students/1600013239')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        respData = self.client.post('/user/students')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        respData = self.client.put('/user/students')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        respData = self.client.delete('/user/students')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        # Dean login
        respData = self.client.post(
            '/user/login', json.dumps({'uid': 'jyeecs', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # jy info
        jyInfo = {
            'uid': '1600013239',
            'name': "蒋衍",
            'password': '123456',
            'gender': True,
            'dept': 48,
            'grade': 2017,
        }

        yzyInfo = {
            'uid': '1700012855',
            'name': 'YuZiyi',
            'password': '123456',
            'gender': True,
            'dept': 48,
            'grade': 2017,
        }

        # Dean create user - param error
        respData = self.client.post(
            '/user/students', json.dumps(jyInfo), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.PARAM_ERR)

        # Dean create user - OK
        respData = self.client.post(
            '/user/students', json.dumps({'students': [jyInfo, yzyInfo, ]}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Dean create user - Duplicate creation
        respData = self.client.post(
            '/user/students', json.dumps({'students': [jyInfo, ]}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.USER_DUP)

        # Dean get all user info
        respData = self.client.get('/user/students')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(type(resp.get('data')), list)
        self.assertEqual(len(resp.get('data')), 3)

        # Dean logout
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Should successfully logout
        respData = self.client.get('/user/students/1600013239')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        # JY login
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1600013239', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # JY get info - OK
        respData = self.client.get('/user/students/1600013239')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # JY is not authorized to operate others' info
        respData = self.client.get('/user/students/1700012855')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        respData = self.client.post(
            '/user/students', json.dumps({'students': []}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        respData = self.client.delete('/user/students/1700012855')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        # JY logout
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # YZY login
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1700012855', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # YZY logout
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Dean login again!!!
        respData = self.client.post(
            '/user/login', json.dumps({'uid': 'jyeecs', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Dean edit student info - uid can not be null
        respData = self.client.put(
            '/user/students', json.dumps({'name': 'JY', 'password': '12345678'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.PARAM_ERR)

        # Dean edit student info - nonexist user
        respData = self.client.put(
            '/user/students/1600099999', json.dumps({'name': 'JY', 'password': '123456789'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.USER_404)

        # Dean edit student info - OK
        respData = self.client.put(
            '/user/students/1600013239', json.dumps({'name': 'JY', 'password': '12345678'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Dean delete student - OK
        respData = self.client.delete('/user/students/1700012855')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Dean logout
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # JY login, find his password has been changed!
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1600013239', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.AUTH_FAIL)

        # JY uses new password to login
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1600013239', 'password': '12345678'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # JY sees his name has been changed
        respData = self.client.get('/user/students/1600013239')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(type(resp.get('data')), list)
        self.assertEqual(len(resp.get('data')), 1)
        self.assertEqual(type(resp.get('data')[0]), dict)
        self.assertEqual(resp.get('data')[0].get('name'), 'JY')

        # JY logout
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # YZY login fails (has been deleted)
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1700012855', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), False)
        self.assertEqual(resp.get('msg'), ERR_TYPE.AUTH_FAIL)
