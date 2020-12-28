<template>
<el-main>
    <el-form :model="formInline" class="form-inline" size="mini" label-width="auto" ref="formInline">
    <el-row  type="flex" gutter="20" justify="center">
        <el-col span="4">
        <el-form-item label="课程编号" prop="id">
            <el-input v-model="formInline.id" placeholder="课程编号" onkeyup="this.value=this.value.replace(/\D/g,'')" onafterpaste="this.value=this.value.replace(/\D/g,'')"></el-input>
        </el-form-item>
        </el-col>
        <el-col span="4">
        <el-form-item label="课程名称" prop="name">
            <el-input v-model="formInline.name" placeholder="课程名称"></el-input>
        </el-form-item>
        </el-col>
         <el-col span="4">
            <el-form-item label="课程院系" prop="dept">
                <el-select v-model="formInline.dept" placeholder="院系名称">
                <el-option v-for=" (name,nameIndex) in this.department" :key="nameIndex" :label="name.name" :value="name.id"></el-option>
                </el-select>
            </el-form-item>
         </el-col>
    </el-row>
    <el-row  type="flex" gutter="20" justify="center">
        <el-col span="8">
            <el-form-item label="课程时间" prop="date">
                <el-select v-model="formInline.date" placeholder="日期">
                    <el-option v-for=" (name,nameIndex) in this.date" :key="nameIndex" :label="name" :value="name"></el-option>
                </el-select>
                <el-select v-model="formInline.lesson" multiple placeholder="时间">
                    <el-option v-for=" (name,nameIndex) in this.lessons" :key="nameIndex" :label="name" :value="name"></el-option>
                </el-select>
            </el-form-item>
        </el-col>
    </el-row>
    <el-row type="flex" gutter="20" justify="center">
        <el-col span="8">
            <el-form-item label="课程类别" prop="Mainclass">
                <el-select v-model="formInline.Mainclass" @change="formInline.Subclass=''" placeholder="课程类别">
                    <el-option v-for=" (name,nameIndex) in this.Mainclass" :key="nameIndex" :label="name" :value="name"></el-option>
                </el-select>
                <el-select v-if="formInline.Mainclass==='通选课'" v-model="formInline.Subclass" placeholder="课程类别">
                    <el-option label="A" value="A"></el-option>
                    <el-option label="B" value="B"></el-option>
                    <el-option label="C" value="C"></el-option>
                    <el-option label="D" value="D"></el-option>
                    <el-option label="E" value="E"></el-option>
                    <el-option label="F" value="F"></el-option>
                </el-select>
                <el-select v-if="formInline.Mainclass==='英语课'" v-model="formInline.Subclass" placeholder="课程类别">
                    <el-option label="A" value="A"></el-option>
                    <el-option label="B" value="B"></el-option>
                    <el-option label="C" value="C"></el-option>
                    <el-option label="C+" value="C+"></el-option>
                </el-select>
            </el-form-item>
        </el-col>
        <el-col span="5">
            <el-form-item>
                <el-row>
                    <el-button type="primary" @click="onSubmit">查询</el-button>
                    <el-button type="info" @click="refresh">清空</el-button>
                </el-row>
            </el-form-item>
        </el-col>
    </el-row>

    </el-form>
    <el-row v-if="this.OnSearch===true">
        <el-table style="width: 100%;"
                    :data="courseList.slice((currentPage-1)*pagesize,currentPage*pagesize)">
            <el-table-column type="index" width="50"></el-table-column>
            <el-table-column label="编号" prop="course_id" width="90"></el-table-column>
            <el-table-column label="名称" prop="name" width="120"></el-table-column>
            <el-table-column label="开课时间" prop="time" width="180"></el-table-column>
            <el-table-column label="学分" prop="credit" width="90"></el-table-column>
            <el-table-column label="讲师" prop="lecturer" width="120"></el-table-column>
            <el-table-column label="地点" prop="pos" width="180"></el-table-column>
            <el-table-column label="选课状态" prop="state" width="180"></el-table-column>
            <el-table-column label="选课操作" fixed="right">
             <template slot-scope="scope">
                <el-row><el-link type="primary" :href="'stuCourseDetail/'+courseList[(currentPage-1)*pagesize+scope.$index].course_id">详细信息</el-link></el-row>
                <el-row v-if="courseList[(currentPage-1)*pagesize+scope.$index].election.status===0" type="flex" gutter="20" justify="left">
                    <el-col :span="6">
                        <el-input v-model="courseList[(currentPage-1)*pagesize+scope.$index].election.willpoint" placeholder="意愿点" size="mini" width="100"></el-input>
                    </el-col>
                    <el-col :span="4">
                        <el-button @click="handleClick(scope.$index,0)" type="primary" size="mini">选课</el-button>
                    </el-col>
                </el-row>
                <el-row v-if="courseList[(currentPage-1)*pagesize+scope.$index].election.status===2" type="flex" gutter="20" justify="left">
                    <el-col :span="6">
                        <el-input v-model="courseList[(currentPage-1)*pagesize+scope.$index].election.willpoint" placeholder="意愿点" size="mini" width="100"></el-input>
                    </el-col>
                    <el-col :span="4">
                        <el-button @click="handleClick(scope.$index,1)" type="primary" size="mini">修改</el-button>
                    </el-col>
                    <el-col :span="4">
                        <el-popover placement="bottom"
                                width="100"
                                triger="click"
                                v-model="visible"
                                >
                                <div style="text-align: center; margin: 0">
                                    <p>是否决定退课？</p>
                                    <el-button type="primary" size="mini" @click="handleClick(scope.$index,2)">确定</el-button>
                                </div>
                            <el-button size=mini type="danger" slot="reference">退课</el-button>
                        </el-popover>
                    </el-col>
                </el-row>
                <el-row v-if="courseList[(currentPage-1)*pagesize+scope.$index].election.status===1" type="flex" gutter="20" justify="left">
                    <el-col :span="6">
                        <el-input v-model="courseList[(currentPage-1)*pagesize+scope.$index].election.willpoint" :disabled="true" placeholder="意愿点" size="mini" width="100"></el-input>
                    </el-col>
                    <el-col :span="4">
                        <el-popover placement="bottom"
                                width="100"
                                triger="click"
                                v-model="visible"
                                >
                                <div style="text-align: center; margin: 0">
                                    <p>是否决定退课？</p>
                                    <el-button type="primary" size="mini" @click="remove(courseIndex,lessonIndex)">确定</el-button>
                                </div>
                            <el-button size=mini type="danger" slot="reference">退课</el-button>
                        </el-popover>
                    </el-col>
                </el-row>
            </template>
            </el-table-column>
        </el-table>
        <el-pagination
            background
            layout="total, sizes, prev, pager, next, jumper"
            :total="this.courseList.length"
            @current-change="handleCurrentChange"
            @size-change="handleSizeChange"
            :current-page="currentPage"
            :page-sizes="[5, 10, 20, 40]"
            :page-size="pagesize"
            >
        </el-pagination>
    </el-row>
    <!-- <div>{{courseList}}</div> -->
</el-main>
</template>
<script>
import axios from 'axios'
export default {
  data () {
    return {
      formInline: {
        name: '',
        id: '',
        dept: '',
        date: '',
        lesson: [],
        Mainclass: '',
        Subclass: ''
      },
      OnSearch: false,
      department: ['信科', '不是信科'],
      currentPage: 1,
      // 初始页
      pagesize: 10,
      // 每页的数据
      courseList: [
        {
          'course_id': 1233343,
          'class_no': 1,
          'name': '软件工程',
          'credit': 4,
          'times': [
            {'day': 2, 'period': [3, 4]},
            {'day': 4, 'period': [5, 6]}
          ],
          'time': '周二吃早饭',
          'lecturer': '孙艳春',
          'pos': '理教201',
          'dept': 48,
          'election': {
            'status': 1,
            'willpoint': 99,
            'elected_num': 121,
            'capacity': 150,
            'pending_num': 13
          }
        }
      ],
      all: 2,
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
  },
  mounted () {
    this.OnSearch = false
    axios.get('http://39.98.75.17:8000/courses/depts', {withCredentials: true}).then(response => {
      this.department = response.departments
    })
  },
  methods: {
    onSubmit () {
      console.log('submit!')
      // test for fore-end start
      var period = ''
      for (let j = 0; j < this.formInline.lesson.length; ++j) {
        for (let i = 0; i < this.lessons.length; ++i) {
          if (this.formInline.lesson[j] === this.lessons[i]) {
            if (period !== '') {
              period = period + ',' + (i + 1).toString()
            } else {
              period = (i + 1).toString()
            }
          }
        }
      }
      console.log(period)
      let day = (this.date.lastIndexOf(this.formInline.date) + 1).toString()
      console.log(day)
      if (day === '0') {
        day = ''
      }
      let mainclass = this.Mainclass.lastIndexOf(this.formInline.Mainclass).toString()
      if (mainclass === '-1') {
        mainclass = ''
      }
      axios.get('http://39.98.75.17:8000/course/courses?id=' + this.formInline.id +
          '&period=' + period + '&day=' + day + '&name=' + this.formInline.name +
          '&main_class=' + mainclass + '&sub_class=' + this.formInline.Subclass +
          '&dept=' + this.formInline.dept, {withCredentials: true}).then(response => {
        return response.data
      }).then(data => {
        this.courseList = data.course_list
        console.log(this.courseList)
        this.currentPage = 1
        for (let i = 0; i < this.pagesize && i < this.courseList.length; i++) {
          this.$set(this.courseList[i], 'time', '')
          for (let j = 0; j < this.courseList[i].times.length; ++j) {
            this.courseList[i].time += this.date[this.courseList[i].times[j].day - 1]
            for (let k = 0; k < this.courseList[i].times[j].period.length; ++k) {
              this.courseList[i].time += this.lessons[this.courseList[i].times[j].period[k] - 1] + ','
            }
            this.courseList[i].time += '\n'
          }
          // console.log(i)
          let key = 'state'
          let value = this.courseList[i].election.elected_num.toString() + '/' +
            this.courseList[i].election.capacity.toString() + ' 待抽签人数:' +
            this.courseList[i].election.pending_num.toString()
          this.$set(this.courseList[i], key, value)
        }
        this.OnSearch = true
      // test for fore-end end
      })
      console.log(this.courseList)
    },
    refresh () {
      this.formInline = {
        name: '',
        id: '',
        dept: '',
        date: '',
        lesson: '',
        Mainclass: '',
        Subclass: ''
      }
    },
    handleClick (row, type) {
      axios.post('http://39.98.75.17:8000/election/elect',
        {'course_id': this.courseList[(this.currentPage - 1) * this.pagesize + row],
          'willingpoint': Number(this.courseList[(this.currentPage - 1) * this.pagesize + row].election.willpoint),
          'type': type},
        {withCredentials: true}).then(this.$router.go(0))
    },
    handleCurrentChange (currentPage) {
      this.currentPage = currentPage
      console.log(this.currentPage)
      for (let i = (currentPage - 1) * this.pagesize; i < currentPage * this.pagesize && i < this.courseList.length; i++) {
        this.courseList[i]['time'] = ''
        for (let curTime in this.courseList[i].times) {
          this.courseList[i].time += this.date[curTime.day - 1]
          for (let period in curTime.period) {
            this.courseList[i].time += this.lessons[period - 1] + ','
          }
          this.courseList[i].time += '\n'
        }
        let key = 'state'
        let value = this.courseList[i].election.elected_num.toString() + '/' +
          this.courseList[i].election.capacity.toString() + ' 待抽签人数:' +
          this.courseList[i].election.pending_num.toString()
        this.courseList[i][key] = value
      }
    }
  }
}
</script>
