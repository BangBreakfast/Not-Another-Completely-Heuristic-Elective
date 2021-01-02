from django.test import TestCase
from .models import Course
from user.models import User
import json
from elect_system.settings import ERR_TYPE
from .views import check_time_format
#用于course类的测试类
class CourseTests(TestCase):
    def test_courses(self):
        # 首先创建一个用于添加、修改课程的教务账户
        u = User.objects.create_user('jyeecs', password='123456')
        u.is_superuser = True
        u.save()

        # 教务完成登陆操作
        respData = self.client.post(
            '/user/login', json.dumps({'uid': 'jyeecs', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 教务添加五个测试用的课程
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
            "course_id": 4830010,
            "name": "信息科学技术概论",
            "credit": 1,
            "main_class": 0,
            "sub_class": "A",
            "times": [
                {"day": 1, "period": [7, 8]}
            ],
            "lecturer": "王源",
            "pos": "理教201",
            "dept": 48,
            "detail": "本课程属讲座课，主要由信息科学技术学院各主要研究方向的知名教授讲授信息科学技术各个学科方向的发展历史、发展现状、相关领域基础知识以及发展趋势等方面的内容。同学通过课程的学习能够对信息科学技术领域包含的各个学科、各个领域有一个整体的、全面的了解；使学生对计算机软件、计算机体系结构、计算机理论、纳米电子学、量子电子学、通讯技术、微电子学、智能科学等学科门类有一个比较明确的概念。",
            "capacity": 150,
        }

        crs2 = {
            "course_id": 4830550,
            "name": "存储技术基础",
            "credit": 2,
            "main_class": 0,
            "sub_class": "A",
            "times": [
                {"day": 2, "period": [3, 4]}
            ],
            "lecturer": "汪小林,罗英伟",
            "pos": "待定",
            "dept": 48,
            "detail": "现代信息管理面临信息量大、管理成本居高不下等诸多挑战。本课程从信息管理的复杂性与现实需求出发，介绍了满足现代信息管理需求的存储技术基础知识，从而使同学们对存储有一个全面的了解。课程介绍了存储系统的构成和基本原理，并在此基础上介绍了几种不同的网络存储构架以及不同的应用环境。从需求出发，本课程还介绍了业务连续性对企业的重要价值与实现形式。最后，本课程介绍了数据中心的监测、管理的原理、方法与实现。通过本课程的学习，同学们能够对存储技术有一个全面的了解，这不仅有利于同学们在存储技术领域的发展，同时，对于同学们将来在企业、政府机关中所进行信息管理的规划、决策等方面的工作也颇有助益。"
                        "另一方面，虚拟化技术正成为全球的热点话题，本课程也将介绍系统级虚拟化的原理、方法及应用，同时还将介绍虚拟化技术最新的进展，以及它如何改善现代计算系统的可靠性、可管理性、有效性以及安全性。"
                        "本课程是我们与EMC、VMWare和Intel等公司共同建设的，三个在业界领先的公司也将为本课程提供先进的软硬件产品，为本课程构建一个良好的实践环境。同时，本课程还会邀请三个公司的高级技术人员为同学们举行实际应用案例讲座。",
            "capacity": 80,
        }

        crs3 = {
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

        crs4 = {
            "course_id": 430109,
            "name": "演示物理学",
            "credit": 2,
            "main_class": 5,
            "sub_class": "A",
            "times": [
                {"day": 2, "period": [1, 2]}
            ],
            "lecturer": "李湘庆",
            "pos": "待定",
            "dept": 4,
            "detail": "课程采取以实验贯穿教学组织方式进行教学。具体作法是，精选若干演示试验，组织学生观察现象，提出问題，讲解相关的物理规律，引导学生感悟物理学的精髓，使学生对物理学获得一个初步而准确的整体印象，作为今后自身扩展科技知识的基础。",
            "capacity": 120,
        }

        # 这里展示一些错误的时间段参数，分别代表“缺少日期”、“上课时间段格式错误”，“上课时间段数值越界”，“日期错误”
        testTimes0 = [
            {"period": [3,4]},
        ]
        testTimes1 = [
            {"day":2, "period":3},
        ]
        testTimes2 = [
            {"day":2, "period":[3,20]},
        ]
        testTimes3 = [
            {"day":8, "period":[3,4]},
        ]
        self.assertEqual(check_time_format(testTimes0), False)
        self.assertEqual(check_time_format(testTimes1), False)
        self.assertEqual(check_time_format(testTimes2), False)
        self.assertEqual(check_time_format(testTimes3), False)
        self.assertEqual(check_time_format(crs0['times']), True)

        # 请求格式错误，正确格式应当为{course：[course1,course2......]}
        respData = self.client.post(
            '/course/courses', json.dumps(crs0), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.PARAM_ERR)

        # 请求格式正确
        respData = self.client.post(
            '/course/courses', json.dumps({'courses': [crs0, crs1, crs2, crs3, crs4]}), content_type="application/json")
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)

        # 课程重复添加
        respData = self.client.post(
            '/course/courses', json.dumps({'courses': [crs0, ]}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.COURSE_DUP)

        # 对课程进行搜索（采用复合的搜索查询条件）
        respData = self.client.get('/course/courses')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(type(resp.get('course_list')), list)
        self.assertEqual(len(resp.get('course_list')), 5)

        # Dean edit course (Not implemented yet)
        # param error
        # edit nonexist
        # OK

        # 教务依照课程的id来进行课程的搜寻
        respData = self.client.get('/course/courses?id=4830550')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(len(resp.get('course_list')), 1)
        self.assertEqual(resp.get('course_list')[0].get('name'), '存储技术基础')
        #教务依照课程的开课院系来进行课程的搜寻
        respData = self.client.get('/course/courses?dept=4')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(len(resp.get('course_list')), 2)
        #教务依照课程的课程类别来进行课程的搜寻
        respData = self.client.get('/course/courses?main_class=5')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(len(resp.get('course_list')), 1)

        # 教务删除课程
        respData = self.client.delete('/course/courses/1233346')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 教务搜索课程
        respData = self.client.get('/course/courses?dept=48')
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(len(resp.get('course_list')), 2)

        # 教务添加一个学生用户用于测试
        jyInfo = {
            'uid': '1600013239',
            'name': "蒋衍",
            'password': '123456',
            'gender': True,
            'dept': 48,
            'grade': 2017,
        }
        respData = self.client.post(
            '/user/students', json.dumps({'students': [jyInfo, ]}), content_type="application/json")
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

        # 学生登入系统进行测试
        respData = self.client.post(
            '/user/login', json.dumps({'uid': '1600013239', 'password': '123456'}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('success'), True)

        # 学生按照课程开课院系进行查询
        respData = self.client.get('/course/courses?dept=4')
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(len(resp.get('course_list')), 2)
        #设置多个查询条件进行课程查询
        respData = self.client.get('/course/courses?dept=4&main_class=0')
        resp = respData.json()
        if resp.get('msg') is not None:
            print("Error msg: " + str(resp.get('msg')))
        self.assertEqual(resp.get('success'), True)
        self.assertEqual(len(resp.get('course_list')), 1)
        self.assertEqual(resp.get('course_list')[0].get('name'), '天体物理专题')

        # 学生没有删除/修改课程的权限
        respData = self.client.post(
            '/course/courses', json.dumps({'courses': [crs0, ]}), content_type="application/json")
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)

        respData = self.client.delete('/course/courses/1233346')
        resp = respData.json()
        self.assertEqual(resp.get('msg'), ERR_TYPE.NOT_ALLOWED)
