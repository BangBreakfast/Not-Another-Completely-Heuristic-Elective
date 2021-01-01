from django.http.response import JsonResponse
from django.test import TestCase
from .models import User
from elect_system.settings import ERR_TYPE
import json
#测试类，用于对user类的功能实现测试

class UserTests(TestCase):
    #login操作的测试
    def test_login(self):
        u = User.objects.create_user('1500012345', password='123456')
        u.save()
        u = User.objects.create_user('1500054321', password='123456')
        u.save()

        # 不合法的请求格式，包括：get、put、delete
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

        # 参数数目的错误，即Post传递的json内容中参数数量错误（只有uid或只有password）
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

        # 密码错误的错误类型
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500012345', 'password': 'zzz'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.AUTH_FAIL)

        # Id不存在的错误类型
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500011111', 'password': '123456'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.AUTH_FAIL)

        # login请求成功
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500012345', 'password': '123456'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 重复进行登录是被允许的
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500012345', 'password': '123456'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 同时登录两个账号是被允许的
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1500054321', 'password': '123456'}), content_type="application/json")
        self.assertEqual(type(respData), JsonResponse)
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
    #logout操作的测试
    def test_logout(self):
        u = User.objects.create_user('1500012345', password='123456')
        u.save()

        # logout同样采用post的方式，因此get、put、delete方法均显示模式错误
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

        # logout成功
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
    #测试对学生列表的修改、访问操作
    def test_students(self):
        u = User.objects.create_user('jyeecs', password='123456')
        u.is_superuser = True
        u.save()

        # 没有特权的用户（即学生）无权访问学生信息的列表
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

        # 教务的login操作（教务看作是权限用户）
        respData = self.client.post(
            '/user/login', json.dumps({'uid': 'jyeecs', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 测试用用户信息
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

        # 教务创建学生用户 - 创建格式错误
        respData = self.client.post(
            '/user/students', json.dumps(jyInfo), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.PARAM_ERR)

        # 教务创建学生用户 - 正确格式
        respData = self.client.post(
            '/user/students', json.dumps({'students': [jyInfo, yzyInfo, ]}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 教务创建学生用户 - 重复创建学生返回报错信息
        respData = self.client.post(
            '/user/students', json.dumps({'students': [jyInfo, ]}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.USER_DUP)

        # 教务获取全部学生用户的信息
        respData = self.client.get('/user/students')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(type(resp.get('data')), list)
        self.assertEqual(len(resp.get('data')), 3)

        # 教务退出登录
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 检查教务是否成功完成登出操作（正确时应当不再拥有权限访问）
        respData = self.client.get('/user/students/1600013239')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        # 用户JY进行登录 
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1600013239', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # JY获取个人的信息（成功）
        respData = self.client.get('/user/students/1600013239')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # JY没有获取/修改他人个人信息的权限（包括查看信息、添加学生用户、删除学生用户）
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

        # JY logout登出
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # YZY login登录
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1700012855', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # YZY logout登出
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 教务再次进行登录
        respData = self.client.post(
            '/user/login', json.dumps({'uid': 'jyeecs', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 教务编辑学生的个人信息 - uid不能为空，为空报错
        respData = self.client.put(
            '/user/students', json.dumps({'name': 'JY', 'password': '12345678'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.PARAM_ERR)

        # 教务教务编辑学生的个人信息 - 用户不能不存在
        respData = self.client.put(
            '/user/students/1600099999', json.dumps({'name': 'JY', 'password': '123456789'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.USER_404)

        # 教务教务编辑学生的个人信息 - OK
        respData = self.client.put(
            '/user/students/1600013239', json.dumps({'name': 'JY', 'password': '12345678'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 教务教务编辑学生的个人信息（删除学生） - OK
        respData = self.client.delete('/user/students/1700012855')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # Dean logout登出
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # JY 登录, 发现他的个人密码被修改
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1600013239', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.AUTH_FAIL)

        # JY 使用新的密码完成登陆操作
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1600013239', 'password': '12345678'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # JY 发现他的名字已经被修改过
        respData = self.client.get('/user/students/1600013239')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(type(resp.get('data')), list)
        self.assertEqual(len(resp.get('data')), 1)
        self.assertEqual(type(resp.get('data')[0]), dict)
        self.assertEqual(resp.get('data')[0].get('name'), 'JY')

        # JY 登出
        respData = self.client.post('/user/logout')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # YZY 登陆失败 (该用户已经被删除)
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1700012855', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), False)
        self.assertEqual(resp.get('msg'), ERR_TYPE.AUTH_FAIL)
