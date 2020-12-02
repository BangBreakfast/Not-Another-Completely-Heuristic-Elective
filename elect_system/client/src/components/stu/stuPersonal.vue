<template>
    <div class="class-table">
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
                                <p>{{'第' + digital2Chinese(lessonIndex+1) + "节"}}</p>
                                <p class="period">{{ lesson }}</p>
                            </td>

                            <td v-for="(course, courseIndex) in classTableData.courses" :key="courseIndex">
                                <el-row>{{classTableData.courses[courseIndex][lessonIndex]|| '-'}}</el-row>
                                <span class="willpoint" v-if="classTableData.courses[courseIndex][lessonIndex]!==''">意愿点：{{classTableData.willing[courseIndex][lessonIndex]}}</span>
                                <el-row>
                                    {{classTableData.details[courseIndex][lessonIndex]|| '-'}}
                                </el-row>
                                <el-popover placement="bottom"
                                        width="100"
                                        triger="click"
                                        v-if="classTableData.courses[courseIndex][lessonIndex]!==''"
                                        v-model="visible"
                                        >
                                        <div style="text-align: center; margin: 0">
                                            <p class="willpoint">将返还意愿点:{{classTableData.willing[courseIndex][lessonIndex]}}。</p>
                                            <p>是否决定退课？</p>
                                            <el-button type="primary" size="mini" @click="false">确定</el-button>
                                        </div>
                                    <el-button size=mini type="danger" slot="reference">退课</el-button>
                                </el-popover>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
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
          ['生物', '物理', '化学', '政治', '历史', '英语', '', '语文','','','',''],
          ['语文', '数学', '英语', '历史', '', '化学', '物理', '生物','','','',''],
          ['生物', '', '化学', '政治', '历史', '英语', '数学', '语文','','','',''],
          ['语文', '数学', '英语', '历史', '政治', '', '物理', '生物','','','',''],
          ['生物', '物理', '化学', '', '历史', '英语', '数学', '语文','','','',''],
          ['语文', '数学', '英语', '', '', '', '', '','','','',''],
          ['', '', '', '', '', '', '', '','','','','']
        ],
        details:[
          ['fff', '物理', '化学', '政治', '历史', '英语', '', '语文','','','',''],
          ['zzzz', '数学', '英语', '历史', '', '化学', '物理', '生物','','','',''],
          ['miao', '', '化学', '政治', '历史', '英语', '数学', '语文','','','',''],
          ['mer', '数学', '英语', '历史', '政治', '', '物理', '生物','','','',''],
          ['luelue', '物理', '化学', '', '历史', '英语', '数学', '语文','','','',''],
          ['aofuaofu', '数学', '英语', '', '', '', '', '','','','',''],
          ['', '', '', '', '', '', '', '','','','','']
        ],
        willing:[
          ['1', '1', '2', '2', '3', '3', '', '1', '', '', '', ''],
          ['1', '1', '2', '2', '', '3', '4', '2', '', '', '', ''],
          ['1', '', '2', '2', '3', '3', '5', '3', '', '', '', ''],
          ['1', '2', '2', '2', '3', '', '6', '4', '', '', '', ''],
          ['1', '2', '2', '', '3', '5', '6', '5', '', '', '', ''],
          ['1', '2', '2', '', '', '', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '', '', '', '', '', '']
        ]
      }
    }
  },
  created () {
    // /* mock随机数据*/
    // Mock.mock({
    //     lessons: ['08:00-09:00', '09:00-10:00', '10:00-11:00', '11:00-12:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00'],
    //     'courses|7': [['生物', '物理', '化学', '政治', '历史', '英语', '', '语文']]
    // });
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
      return identifier === 'week' && (num === 7) ? '日' : character[num]
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
        }
    }
}
</style>
