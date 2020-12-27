<template>
  <div>
    <h1>{{this.course.name}}</h1>
    <table>
      <tr>
        <td>课程编号</td>
        <td>{{this.course.course_id}}</td>
      </tr>
      <tr>
        <td>课程类别</td>
        <td>{{Mainclass[course.main_class-1]}}</td>
      </tr>
      <tr>
        <td>课程学分</td>
        <td>{{this.course.credit}}</td>
      </tr>
      <tr>
        <td>开课院系</td>
        <td>{{this.course.dept}}</td>
      </tr>
      <tr>
        <td>任课老师</td>
        <td>{{this.course.lecturer}}</td>
      </tr>
      <tr>
        <td>上课地点</td>
        <td>{{this.course.pos}}</td>
      </tr>
      <tr>
        <td>
          <br />上课时间
        </td>
        <td>
          <div v-for="(time,timeIndex) in this.course.times" :key="timeIndex">
            {{date[time.day-1]}}
            <div
              v-for="(lesson,lessonIndex) in time.period"
              :key="lessonIndex"
            >{{lessons[lesson-1]}}</div>
          </div>
        </td>
      </tr>
      <tr>
        <td>详细描述</td>
        <td>{{this.course.detail}}</td>
      </tr>
    </table>
  </div>
</template>

<style>
table {
  width: 100%;
  margin: 0px auto;
}
td {
  box-align: center;
  background-color: azure;
  height: 60px;
}
</style>

<script>
import axios from "axios";
export default {
  mounted() {
    axios
      .get("http://localhost:8000/courses/" + this.$route.params.id, {})
      .then(response => (this.course = response.course));
  },
  data() {
    return {
      course: {
        course_id: 1233343, // From elective.pku.edu.cn
        // "class_no": 1,
        name: "软件工程",
        credit: 4,
        main_class: 1, // 课程类别, 专业课、通选课、体育课等
        sub_class: null, // 通选课类别(ABCDEF) / 英语课类别(ABCC+)，其它大类可缺省
        times: [
          { day: 2, period: [3, 4] },
          { day: 4, period: [5, 6] }
        ],
        lecturer: "孙艳春",
        pos: "理教201",
        dept: 48,
        detail: "About software developing...", // 详细的文字描述
        elect_status: 0 // none / pending / elected
        // "willpoint": 99, feature: 在详情页选课
      },
      lessons: [
        "08:00-08:50",
        "09:00-09:50",
        "10:10-11:00",
        "11:10-12:00",
        "13:00-13:50",
        "14:00-14:50",
        "15:10-16:00",
        "16:10-17:00",
        "17:10-18:00",
        "18:40-19:30",
        "19:40-20:30",
        "20:40-21:30"
      ],
      date: ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
      Mainclass: ["专业课", "政治课", "体育课", "英语课", "通选课"]
    };
  }
};
</script>