from user.models import User
from django.db import models
import sys
import logging
sys.path.append("..")
'''
Course 类

属性:
    course_id: 课程编号
    name: 课程名称
    times: 上课时间(key1：day key2：period)
    credit: 课程学分
    main_class：课程所属大类（包括必修课、限选课、任选课、政治课、英语课、体育课、通选课）
    sub_class：次要类别（例如英语课的ABCC+，通选课的ABCDEF）
    lecture：课程教师
    pos：课程的上课地点
    dept：开课院系
    detail：课程详情
    capacity：课程最大选课人数
    electnum：课程当前选课人数
'''
# 院系列表详细信息
DEPT = [
    {"id":1,"name":"数学科学学院"}, 
    {"id":4,"name":"物理学院"}, 
    {"id":10,"name":"化学院"}, 
    {"id":11,"name":"生命学院"}, 
    {"id":12,"name":"地球与空间科学学院"}, 
    {"id":16,"name":"心理系"}, 
    {"id":17,"name":"软件与微电子学院"}, 
    {"id":18,"name":"新闻与传播学院"}, 
    {"id":19,"name":"应用文理学院"}, 
    {"id":20,"name":"中文系"}, 
    {"id":21,"name":"历史系"}, 
    {"id":22,"name":"考古文博学院"}, 
    {"id":23,"name":"哲学系"}, 
    {"id":24,"name":"国际关系学院"}, 
    {"id":25,"name":"经济学院"}, 
    {"id":28,"name":"光华管理学院"}, 
    {"id":29,"name":"法学院"}, 
    {"id":30,"name":"信息管理系"}, 
    {"id":31,"name":"社会学系"}, 
    {"id":32,"name":"政府管理学院"}, 
    {"id":39,"name":"外国语学院"}, 
    {"id":40,"name":"马克思主义学院"}, 
    {"id":41,"name":"体育教研部"}, 
    {"id":43,"name":"艺术学院"}, 
    {"id":44,"name":"对外汉语教育学院"}, 
    {"id":46,"name":"元培学院"}, 
    {"id":47,"name":"深圳研究生院"},
    {"id":48,"name":"信息科学技术学院"}, 
    {"id":49,"name":"景观设计学研究院"}, 
    {"id":62,"name":"北大国发院"}, 
    {"id":67,"name":"教育学院"}, 
    {"id":68,"name":"人口所"}, 
    {"id":84,"name":"前沿交叉学科研究院"}, 
    {"id":85,"name":"美问题中心"}, 
    {"id":86,"name":"工学院"}, 
    {"id":87,"name":"中古史所"}, 
    {"id":88,"name":"应用化学所"}, 
    {"id":89,"name":"稀土中心"}, 
    {"id":90,"name":"天然产物所"}, 
    {"id":91,"name":"高校化学"}, 
    {"id":92,"name":"岩石圈所"}, 
    {"id":93,"name":"城市开发"}, 
    {"id":94,"name":"历史地理所"}, 
    {"id":95,"name":"天然气中心"}, 
    {"id":96,"name":"心理所"}, 
    {"id":97,"name":"非线性"}, 
    {"id":98,"name":"通信所"}, 
    {"id":99,"name":"图书馆"}, 
    {"id":126,"name":"城市与环境学院"}, 
    {"id":127,"name":"环境科学与工程学院"}, 
    {"id":140,"name":"现代化进程"}, 
    {"id":142,"name":"中外妇女"}, 
    {"id":143,"name":"社会党中心"}, 
    {"id":144,"name":"苏东欧中心"}, 
    {"id":145,"name":"犯罪问题"}, 
    {"id":146,"name":"比较法所"}, 
    {"id":147,"name":"东方文化所"}, 
    {"id":148,"name":"日本中心"}, 
    {"id":149,"name":"世界文学所"}, 
    {"id":150,"name":"中国国情"}, 
    {"id":151,"name":"亚太中心"}, 
    {"id":152,"name":"经济所"}, 
    {"id":153,"name":"科技法中心"}, 
    {"id":155,"name":"美学中心"}, 
    {"id":156,"name":"英语所"}, 
    {"id":157,"name":"海外华经济"}, 
    {"id":158,"name":"社调咨询中心"}, 
    {"id":159,"name":"苏联学所"}, 
    {"id":160,"name":"亚太院"}, 
    {"id":161,"name":"中加中心"}, 
    {"id":163,"name":"持续发展中心"}, 
    {"id":164,"name":"知识产权中心"}, 
    {"id":165,"name":"首都发展研究院"}, 
    {"id":166,"name":"国学研究院"}, 
    {"id":167,"name":"民营经济研究院"}, 
    {"id":168,"name":"中国古文献研究中心"}, 
    {"id":169,"name":"中国古代史研究中心"}, 
    {"id":170,"name":"汉语语言学研究中心"}, 
    {"id":171,"name":"东方文学研究中心"}, 
    {"id":172,"name":"中国考古学研究中心"}, 
    {"id":173,"name":"外国哲学研究所"}, 
    {"id":174,"name":"政治发展与政府管理研究所"}, 
    {"id":175,"name":"中国社会与发展研究中心"}, 
    {"id":176,"name":"邓小平理论研究院"}, 
    {"id":177,"name":"教育经济研究所"}, 
    {"id":178,"name":"经济法研究所"}, 
    {"id":179,"name":"深港产学研基地"}, 
    {"id":181,"name":"科学与工程计算中心"}, 
    {"id":182,"name":"分子医学所"}, 
    {"id":183,"name":"软件工程中心"}, 
    {"id":184,"name":"实验动物中心"}, 
    {"id":185,"name":"先进技术研究院"}, 
    {"id":187,"name":"社会科学调查中心"}, 
    {"id":188,"name":"教育财政科学研究所"}, 
    {"id":189,"name":"科维理研究所"}, 
    {"id":191,"name":"数学中心"}, 
    {"id":192,"name":"歌剧研究院"}, 
    {"id":195,"name":"建筑与景观设计学院"}, 
    {"id":197,"name":"画法研究院"}, 
    {"id":202,"name":"高等人文研究院"}, 
    {"id":203,"name":"麦戈文脑科所"}, 
    {"id":204,"name":"继续教育学院"}, 
    {"id":208,"name":"燕京学堂"}, 
    {"id":213,"name":"中国政治学研究中心"}, 
    {"id":10000,"name":"医学部"}, 
    {"id":10180,"name":"医学部教学办"}, 
    {"id":10801,"name":"医学部院办"}, 
    {"id":10808,"name":"医学部科技处"} ]


class Time(models.Model):
    day = models.IntegerField(default=1)
    period = models.IntegerField(default=1)


class Course(models.Model):
    course_id = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=128, null=True)
    credit = models.IntegerField(blank=False)
    main_class = models.IntegerField(default=1)
    sub_class = models.CharField(max_length=32)
    lecturer = models.CharField(max_length=128)
    pos = models.CharField(max_length=128)
    dept = models.IntegerField(blank=False)

    name_eng = models.CharField(max_length=128, null=True)
    prerequisite = models.CharField(max_length=1024, null=True)
    detail = models.CharField(max_length=1024, null=True)

    capacity = models.IntegerField(default=50)
    elect_num = models.IntegerField(default=0)
    elect_newround_num = models.IntegerField(default=0) # 该属性没有被使用到
    times = models.ManyToManyField(Time)
    #检查课程id是否重复
    def getCourseObj(crsId: str):
        crsSet = Course.objects.filter(course_id=crsId)
        if crsSet.count() != 1:
            logging.error('courseSet size error: courseId={}, size={}'.format(
                crsId, crsSet.count()))
            return None
        return crsSet.get()
    #检查课程id是否合法
    def isLegal(crsId: str) -> bool:
        return Course.objects.filter(course_id=crsId).exists()

