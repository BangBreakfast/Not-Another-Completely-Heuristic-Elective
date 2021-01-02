from django.test import TestCase
from .models import *
from user.models import User
import json
from elect_system.settings import ERR_TYPE, ELE_TYPE

#election类的测试类
class ElectionTests(TestCase):
    def test_elect(self):
        # 创建一个教务用户用于测试
        u = User.objects.create_user('jyeecs', password='123456')
        u.is_superuser = True
        u.save()

        # 教务login登录
        respData = self.client.post(
            '/user/login', json.dumps({'uid': 'jyeecs', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 教务添加三门课程
        crs0 = {
            "course_id": 1233346,
            "name": "软件工程",
            "credit": 4,
            "main_class": 0,
            "sub_class": "A",
            "times": [
                {"day": 2, "period": [3, 4]},
                {"day": 4, "period": [5, 6]}
            ],
            "lecturer": "孙艳春",
            "pos": "理教201",
            "dept": 48,
            "detail": "软件工程是软件工程是计算机科学与技术专业和软件工程专业的专业基础课程，"
                        "本课程旨在系统地介绍软件系统的开发、维护和项目管理的方法、技术和工具，"
                        "培养学生在软件开发、软件维护、项目管理等方面，尤其是在需求捕获与分析、"
                        "软件设计和构造、软件测试等方面的能力，"
                        "使得学生能够在软件开发中灵活应用软件工程方法、技术和工具，"
                        "创建高质量的软件产品。"
                        "软件工程的课程目标如下："
                        "1、使学生掌握软件工程基本思想，包括软件工程目标、软件工程原则及软件工程活动。"
                        "2、使学生掌握软件开发和维护的方法学，了解软件开发过程和软件项目管理基础知识。"
                        "通过案例教学和课程实践培养学生软件开发和维护的能力。"
                        "3、通过课程实践，培养学生软件项目管理的意识，即对一个软件项目的工作量、成本、进度和人员的计划和管理。"
                        "4、培养学生工程素质、创新精神和团队精神。",
            "capacity": 150,
        }

        crs1 = {
            "course_id": 431543,
            "name": "天体物理专题",
            "credit": 3,
            "main_class": 0,
            "sub_class": "A",
            "times": [
                {"day": 1, "period": [1, 2]}
            ],
            "lecturer": "李立新",
            "pos": "待定",
            "dept": 4,
            "detail": "在本课程中，选课学生将参与物理学院天文系或科维理研究所各研究组每周专题讨论会，通过文献阅读、学术讨论，学术报告、专题研究等形式了解当前天体物理最新进展、热点问题，初步掌握天体物理研究的基本方法、手段和资源，训练和培养进行科学研究的基本能力，为后续的论文研究选题打好基础。",
            "capacity": 40,
        }

        crs2 = {
            "course_id": 430109,
            "name": "演示物理学",
            "credit": 2,
            "main_class": 5,
            "sub_class": "A",
            "times": [
                {"day": 2, "period": [3, 4]}
            ],
            "lecturer": "李湘庆",
            "pos": "待定",
            "dept": 4,
            "detail": "课程采取以实验贯穿教学组织方式进行教学。具体作法是，精选若干演示试验，组织学生观察现象，提出问題，讲解相关的物理规律，引导学生感悟物理学的精髓，使学生对物理学获得一个初步而准确的整体印象，作为今后自身扩展科技知识的基础。",
            "capacity": 120,
        }
        respData = self.client.post(
            '/course/courses', json.dumps({'courses': [crs0, crs1, crs2, ]}), content_type="application/json")
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)

        # 教务添加两个学生用户
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
            'name': "于子毅",
            'password': '123456',
            'gender': True,
            'dept': 48,
            'grade': 2017,
        }
        respData = self.client.post(
            '/user/students', json.dumps({'students': [jyInfo, yzyInfo, ]}), content_type="application/json")
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)

        # 教务logout登出
        respData = self.client.post('/user/logout')
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)

        # JY login登入
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1600013239', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # JY 进行课程查询
        respData = self.client.get('/course/courses?dept=4')
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(len(resp.get('course_list')), 2)
        self.assertEqual(resp.get('course_list')[
                         0].get('election').get('status'), 0)
        self.assertEqual(resp.get('course_list')[0].get(
            'election').get('willingpoint'), 0)
        self.assertEqual(resp.get('course_list')[0].get(
            'election').get('elected_num'), 0)
        self.assertEqual(resp.get('course_list')[0].get(
            'election').get('pending_num'), 0)

        # JY获取他人的选课列表
        # 由于权限限制，不允许进行访问
        respData = self.client.get('/election/schedule/1700012855')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        # OK
        respData = self.client.get('/election/schedule')
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(type(resp.get('data')), list)
        self.assertEqual(len(resp.get('data')), 0)

        # Stu 选修一门课程
        # 请求方式GET错误
        respData = self.client.get('/election/elect')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.INVALID_METHOD)

        # 请求方式POST正确，但json格式不正确
        respData = self.client.post(
            '/election/elect', json.dumps({
                'course_id': '1233346',
                'willingpoint': 99
            }), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.PARAM_ERR)

        # 意愿点错误
        respData = self.client.post(
            '/election/elect', json.dumps({
                'type': 0,
                'course_id': '1233346',
                'willingpoint': 101
            }), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.WP_ERR)

        # 正确的请求
        respData = self.client.post(
            '/election/elect', json.dumps({
                'type': 0,
                'course_id': '1233346',
                'willingpoint': 99
            }), content_type="application/json")
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)

        # 时间冲突选课
        respData = self.client.post(
            '/election/elect', json.dumps({
                'type': 0,
                'course_id': '430109',
                'willingpoint': 0
            }), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.TIME_CONF)

        # 意愿点溢出选课
        respData = self.client.post(
            '/election/elect', json.dumps({
                'type': 0,
                'course_id': '431543',
                'willingpoint': 2
            }), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.WP_ERR)

        # 正确选课操作
        respData = self.client.post(
            '/election/elect', json.dumps({
                'type': 0,
                'course_id': '431543',
                'willingpoint': 0
            }), content_type="application/json")
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(Election.getWpCnt('1600013239'), 99)

        # 取消选课操作
        respData = self.client.post(
            '/election/elect', json.dumps({
                'type': 0,
                'course_id': '431543',
                'willingpoint': 0
            }), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.ELE_DUP)

        # Stu获取个人的选课计划
        respData = self.client.get('/election/schedule')
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(type(resp.get('data')), list)
        self.assertEqual(len(resp.get('data')), 2)

        # Stu修改选课的意愿点
        respData = self.client.post(
            '/election/elect', json.dumps({
                'type': 1,
                'course_id': '1233346',
                'willingpoint': 1
            }), content_type="application/json")
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)

        # Stu 意愿点应当得到修改
        self.assertEqual(Election.getWpCnt('1600013239'), 1)
        self.assertEqual(Election.getCourseElecionNum('1233346')[1], 1)
        crss = Election.getCourseOfStudent('1600013239')
        self.assertEqual(type(crss), list)
        self.assertEqual(len(crss), 2)
        self.assertEqual(Election.getStuElectionNum(
            '1600013239', '1233346')[0], ELE_TYPE.PENDING)
        self.assertEqual(Election.getStuElectionNum(
            '1600013239', '1233346')[1], 1)
