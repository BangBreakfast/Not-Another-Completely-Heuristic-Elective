<template>
    <div class="class-table">
    <div class='table-wrapper'>
        <div class="tabel-container">
        <h2 class="header">{{this.course.name}}</h2>
            <el-divider></el-divider>
        <table>
            <tbody>
                <tr>
                    <td class="block">
                        <p>课程编号</p>
                    </td>
                    <td class="block">
                        {{this.course.course_id}}
                    </td>
                </tr>
                <tr>
                    <td class="block">
                        <p>课程类别</p>
                    </td>
                    <td class="block">
                        {{Mainclass[course.main_class-1]}}
                    </td>
                </tr>
                <tr>
                    <td class="block">
                        <p>课程学分</p>
                    </td>
                    <td class="block">
                        {{this.course.credit}}
                    </td>
                </tr>
                <tr>
                    <td class="block">
                        <p>开课院系</p>
                    </td>
                    <td class="block">
                        {{this.course.dept}}
                    </td>
                </tr>
                <tr>
                    <td class="block">
                        <p>任课老师</p>
                    </td>
                    <td class="block">
                        {{this.course.lecturer}}
                    </td>
                </tr>
                 <tr>
                    <td class="block">
                        <p>上课地点</p>
                    </td>
                    <td class="block">
                        {{this.course.pos}}
                    </td>
                </tr>
                <tr>
                    <td class="block">
                        <p>上课时间</p>
                    </td>
                    <td class="block">
                        <el-col :span="24/times" v-for ="(time,timeIndex) in this.course.times" :key="timeIndex">
                            {{date[time.day-1]}}
                            <div v-for ="(lesson,lessonIndex) in time.period" :key="lessonIndex">
                            {{lessons[lesson-1]}}
                            </div>
                        </el-col>
                    </td>
                </tr>
                <tr>
                    <td class="block">
                        <p>详细信息</p>
                    </td>
                    <td class="block">
                        {{this.course.detail}}
                    </td>
                </tr>
            </tbody>
        </table>
        </div>
    </div>
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
    axios.get('http://39.98.75.17:8000/course/depts/', {withCredentials: true}).then(response => (this.dept = response.data.data))
    axios.get('http://39.98.75.17:8000/course/courses/' + this.$route.params.id + '/detail', {withCredentials: true}).then(response => {
      this.course = response.data.course_list[0]
      for (let i = 0; i < this.depts.length; ++i) {
        if (this.depts[i].id === this.course.dept) {
          this.course.dept = this.depts[i].name
          break
        }
      }
    })
  },
  data () {
    return {
      course: {
        'course_id': '1233343',
        'name': '软件工程',
        'credit': 4,
        'main_class': 1,
        'sub_class': null,
        'times': [
          {'day': 2, 'period': [3, 4]},
          {'day': 4, 'period': [5, 6]}
        ],
        'lecturer': '孙艳春',
        'pos': '理教201',
        'dept': 48,
        'detail': 'About software developing...'
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
      ],
      dept: [
        {
          'id': 1,
          'name': '数学院'
        },
        {
          'id': 48,
          'name': '信科'
        }
      ]
    }
  }
}
</script>
<style lang="scss" scoped>
.header{
    // background-color: #67a1ff;
}
.class-table {
    .table-wrapper {
        width: 100%;
        height: 100%;
        overflow: auto;
    }
    .tabel-container {
        margin: 7px;
        width: 100%;
        table {

            table-layout: fixed;
            width:100%;
            thead {
                background-color: #67a1ff;
                th {
                    color: #fff;
                    line-height: 17px;
                    font-weight: bold;
                }
            }
            tbody {
                background-color: #eaf2ff;
                td {
                    color: #677998;
                    line-height: 12px;
                }
            }
            th,
            td {
                width: 60px;
                padding: 12px 2px;
                font-size: 12px;
                text-align: center;
                .willpoint{
                color: #555;
                font-size:  5px;
                padding: 15px 15px auto;
            }
            }

            tr td:first-child {
                color: #333;
                width: 20%;
                background-color: #61a3ff;;
                .period {
                    font-size: 12px;
                }
            }
            tr td:nth-child(2) {
                color: #333;
                width: 80%;
                .period {
                    font-size: 12px;
                }
            }
            .willpoint{
                color: #555;
                font-size:  px;
                padding: 15px 15px auto;
            }
            .coursename{
                font-size: 14px;
                color: #133;
            }
            .block{
                width:65px;
            }
        }
    }
}
</style>
