<template>
    <div>
        <el-row :span="24"><h1>{{this.course.name}}</h1></el-row>
        <el-row>
            <el-col :span="12">课程编号</el-col><el-col :span="12">{{this.course.course_id}}</el-col>
        </el-row>
        <el-row>
            <el-col :span="12">课程类别</el-col>
            <el-col :span="12">
                {{Mainclass[course.main_class-1]}}
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="12">课程学分</el-col><el-col :span="12">{{this.course.credit}}</el-col>
        </el-row>
        <el-row>
            <el-col :span="12">开课院系</el-col><el-col :span="12">信科</el-col>
        </el-row>
        <el-row>
            <el-col :span="12">任课老师</el-col><el-col :span="12">{{this.course.lecturer}}</el-col>
        </el-row>
        <el-row>
            <el-col :span="12">上课地点</el-col><el-col :span="12">{{this.course.pos}}</el-col>
        </el-row>
        <el-row>
            <el-col :span="12">上课时间</el-col>
            <el-col :span="6" v-for ="(time,timeIndex) in this.course.times" :key="timeIndex">
                {{date[time.day-1]}}
                <div v-for ="(lesson,lessonIndex) in time.period" :key="lessonIndex">
                {{lessons[lesson-1]}}
                </div>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="12">详细描述</el-col><el-col :span="12">{{this.course.detail}}</el-col>
        </el-row>
    </div>
</template>

<style>
  .el-row {
    margin-bottom: 40px;
  }
  .el-col {
    border-radius: 4px;
  }
</style>

<script>
import axios from 'axios'
export default {
  mounted () {
    axios.get('http://localhost:8000/course/courses/' + this.$route.params.id + '/detail', {withCredentials: true}).then(response => (this.course = response.data.course_list[0]))
  },
  data () {
    return {
      course: {
        'course_id': 1233343,
        'name': '软件工程',
        'credit': 4,
        "main_class": 1,
                "sub_class": null,   // 通选课类别(ABCDEF) / 英语课类别(ABCC+)，其它大类可缺省
                "times": [
                    {"day":2, "period":[3,4]},
                    {"day":4, "period":[5,6]},
                ],
                "lecturer": "孙艳春",
                "pos": "理教201",
                "dept": 48,
                "detail": "About software developing...",     // 详细的文字描述
                "elect_status": 0,    // none / pending / elected
                // "willpoint": 99, feature: 在详情页选课
            },
            lessons: [
                '08:00-08:50',
                '09:00-09:50',
                '10:10-11:00',
                '11:10-12:00',
                '13:00-13:50',
                '14:00-14:50',
                '15:10-16:00',
                '16:10-17:00',
                '17:10-18:00',
                '18:40-19:30',
                '19:40-20:30',
                '20:40-21:30'
            ],
            date: [
                '周一',
                '周二',
                '周三',
                '周四',
                '周五',
                '周六',
                '周日'
            ],
            Mainclass: [
                '专业课',
                '政治课',
                '体育课',
                '英语课',
                '通选课'
            ]
        }
    }
}
</script>
