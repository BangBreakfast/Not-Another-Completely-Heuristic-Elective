<template>
    <div class="class-table">

        <el-row>
            您剩余的意愿点:{{will}}
        </el-row>
        <el-divider></el-divider>
        <div class="table-wrapper">
            <div class="tabel-container">

                <table>
                    <thead>
                        <tr>
                            <th>时间</th>
                            <th v-for="(weekNum, weekIndex) in classTableData.courses.length" :key="weekIndex"> {{'周' + digital2Chinese(weekIndex, 'week')}}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(lesson, lessonIndex) in classTableData.lessons" :key="lessonIndex">
                            <td>
                                <p>{{'第' + digital2Chinese(lessonIndex) + "节"}}</p>
                                <p class="period">{{ lesson }}</p>
                                
                            </td>

                            <td v-for="(course, courseIndex) in classTableData.courses" :key="courseIndex">
                                <el-link type="primary" :href="'stuCourseDetail/'+classTableData.id[courseIndex][lessonIndex]">{{classTableData.courses[courseIndex][lessonIndex]|| '-'}}</el-link>
                                <el-row v-if="classTableData.courses[courseIndex][lessonIndex]!=='' && classTableData.election_status[courseIndex][lessonIndex]==2">
                                    <el-col v-if="classTableData.courses[courseIndex][lessonIndex]!==''">
                                        <span class="willpoint">意愿点：</span>
                                        <el-input type="number" size="mini" oninput="if(value>99=99;if(value<0)value=0" v-model="classTableData.willing[courseIndex][lessonIndex]" max="100" min="0" class="block">
                                        </el-input>
                                    </el-col>
                                    <el-col>
                                        <el-button size=mini type="primary" @click="modify(courseIndex,lessonIndex)" >修改</el-button>
                                        <el-popover placement="bottom"
                                            width="100"
                                            triger="click"
                                            v-model="visible"
                                            >
                                            <div style="text-align: center; margin: 0">
                                                <p>是否决定把课程从选课队列中移除？</p>
                                                <el-button type="primary" size="mini" @click="remove(courseIndex,lessonIndex)">确定</el-button>
                                            </div>
                                        <el-button size=mini type="danger" slot="reference">退课</el-button>
                                        </el-popover>
                                    </el-col>
                                </el-row>
                                <el-row v-if="classTableData.courses[courseIndex][lessonIndex]!==''&&classTableData.election_status[courseIndex][lessonIndex]==1">
                                    <el-col v-if="classTableData.courses[courseIndex][lessonIndex]!==''">
                                        <span class="willpoint">意愿点：</span>
                                        <el-input type="number" size="mini" disabled="true" oninput="if(value>99=99;if(value<0)value=0" v-model="classTableData.willing[courseIndex][lessonIndex]" max="100" min="0" class="block">
                                        </el-input>
                                    </el-col>
                                    <el-popover placement="bottom"
                                        width="100"
                                        triger="click"
                                        v-model="visible"
                                        >
                                        <div style="text-align: center; margin: 0">
                                            <p>将返回意愿点{{classTableData.willing[courseIndex][lessonIndex]}}</p>
                                            <p>是否决定退课？</p>
                                            <el-button type="primary" size="mini" @click="drop(courseIndex,lessonIndex)">确定</el-button>
                                        </div>
                                    <el-button size=mini type="danger" slot="reference">退课</el-button>
                                </el-popover>
                                </el-row>
                                <el-row> {{classTableData.details[courseIndex][lessonIndex]|| '-'}}</el-row>
                                <el-row> {{classTableData.election_detail[courseIndex][lessonIndex]|| '-'}}</el-row>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {getCookie} from '../../assets/js/cookies.js'
export default {
  data () {
    return {
      dept: [],
      will: 99,
      classTableData: {
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
        courses: [
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', '']
        ],
        details: [
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', '']
        ],
        willing: [
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', '']
        ],
        election_status: [
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', '']
        ],
        election_detail: [
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', '']
        ],
        id: [
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', '']
        ]
      }
    }
  },
  mounted () {
    let username = getCookie('username').substring(3)
    // console.log(getCookie('username'))
    axios.get('http://39.98.75.17:8000/election/schedule/' + username, {withCredentials: true}).then(response => {
      return response.data
    }).then(data => {
      if (data.success === true) {
        data = data.data
        console.log(data)
        for (let i = 0; i < data.length; ++i) {
          console.log(data[i].times.length)
          let course = data[i]
          this.will -= course.election.willingpoint
          for (let j = 0; j < data[i].times.length; ++j) {
            let day = data[i].times[j].day - 1
            console.log('d')
            console.log(day)
            for (let k = 0; k < course.times[j].period.length; ++k) {
              let period = course.times[j].period[k] - 1
              console.log('p')
              console.log(period)
              this.classTableData.id[day][period] = course.course_id.toString()
              this.classTableData.courses[day][period] = course.course_id.toString() + ':' + course.name
              this.classTableData.details[day][period] = '学分:' + course.credit
              this.classTableData.details[day][period] = this.classTableData.details[day][period] + '\n讲师' + course.lecturer
              this.classTableData.details[day][period] = this.classTableData.details[day][period] + '\n教室' + course.pos
              this.classTableData.willing[day][period] = course.election.willingpoint
              this.classTableData.election_status[day][period] = course.election.status
              this.classTableData.election_detail[day][period] = '已选人数:' + course.election.elected_num.toString() + '\n课程容量' + course.election.capacity.toString() + '\n待抽签人数' + course.election.pending_num.toString()
            }
          }
        }
        console.log(this.classTableData)
        this.$forceUpdate()
      } else {
        alert(data.msg)
      }
    })
  },
  methods: {
    /**
    * 数字转中文
    * @param {Number} num 需要转换的数字
    * @param {String} identifier 标识符
    * @returns {String} 转换后的中文
    */
    digital2Chinese (num, identifier) {
      const character = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三']
      return identifier === 'week' && (num === 6) ? '日' : character[num]
    },
    modify (courseIndex, lessonIndex) {
      axios.post('http://39.98.75.17:8000/election/elect', {'course_id': this.classTableData.id[courseIndex][lessonIndex], 'willingpoint': Number(this.classTableData.willing[courseIndex][lessonIndex]), 'type': 1}, {withCredentials: true}).then(response => (this.$router.go(0)))
    },
    remove (courseIndex, lessonIndex) {
      axios.post('http://39.98.75.17:8000/election/elect', {'course_id': this.classTableData.id[courseIndex][lessonIndex], 'willingpoint': Number(this.classTableData.willing[courseIndex][lessonIndex]), 'type': 2}, {withCredentials: true}).then(response => (this.$router.go(0)))
    },
    drop (courseIndex, lessonIndex) {
      axios.post('http://39.98.75.17:8000/election/elect', {'course_id': this.classTableData.id[courseIndex][lessonIndex], 'willingpoint': Number(this.classTableData.willing[courseIndex][lessonIndex]), 'type': 3}, {withCredentials: true}).then(response => (this.$router.go(0)))
    }
  }
}
</script>

<style lang="scss" scoped>
.class-table {
    .table-wrapper {
        width: 100%;
        height: 100%;
        overflow: auto;
    }
    .tabel-container {
        margin: 7px;
        table {

            table-layout: fixed;
            width: 100%;

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
                .period {
                    font-size: 8px;
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
