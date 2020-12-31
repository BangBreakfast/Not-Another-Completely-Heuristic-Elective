# Not-Another-Completely-Heuristic-Elective

> 组长：**高立人**

## 项目介绍

北京大学多轮抽签选课系统

## 主要功能

教务：
 - 增删改课程
 - 增删学生
 - 管理抽签时间

学生：
 - 登录、退出、修改密码
 - 按条件检索课程
 - 查看个人课表
 - 选课、修改意愿点、退出等待队列、退课
 - 查看抽签结果

技术选型：
前端使用 vue，后端使用 Django + MySQL

## 部署启动
1. 准备数据库
 - 安装 MySQL version >= 5.7
 - 创建 elective 数据库，字符集需要支持 utf8

2. 后端部署与启动
 - git clone 本项目源代码，在 elect_system/settings.py 中输入数据库密码与邮箱密码
 - 安装 django 及依赖包：`pip install django pymysql django-apscheduler`
 - 迁移数据库：`python manage.py makemigrations && python manage.py migrate`
 - 后端启动：`python manage.py runserver 0.0.0.0:8000`

3. 前端部署与启动
 - 切换到前端路径``cd elect_system/client``
 - 安装全部依赖包``npm install``
 - 前端启动``npm run dev``
 - 如果按照上述方法不能启动，直接下载我们打包好的elect_system.tar(联系gaoliren@pku.edu.cn)，则不需要运行``npm install``
 - 根据提示可能需要运行``npm rebuild node-sass``再运行``npm run dev``