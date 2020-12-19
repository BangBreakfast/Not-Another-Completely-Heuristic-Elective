<template>
    <div>
        <table>
            <el-row><h1>{{course.name}}</h1></el-row>
            <el-row>
                <el-col class="col1">课程ID</el-col><el-col class="col2"><el-input type="textarea" :placeholder="this.course.course_id" v-model="this.course.course_id"></el-input></el-col>
            </el-row>
            <el-row>
                <el-col class="col1">班号</el-col><el-col class="col2"><el-input type="textarea" :placeholder="this.course.class_no" v-model="this.course.class_no"></el-input></el-col>
            </el-row>
            <el-row>
                <el-col class="col1">学分</el-col><el-col class="col2"><el-input type="textarea" :placeholder="this.course.credit" v-model="this.course.credit"></el-input></el-col>
            </el-row>
            <el-row>
                <el-col class="col1">开课院系</el-col><el-col class="col2"><el-input type="textarea" :placeholder="this.course.dept" v-model="this.course.dept"></el-input></el-col>
            </el-row>
            <el-row>
                <el-col class="col1">任课老师</el-col><el-col class="col2"><el-input type="textarea" :placeholder="this.course.lecturer" v-model="this.course.lecturer"></el-input></el-col>
            </el-row>
            <el-row>
                <el-col class="col1">上课地点</el-col><el-col class="col2"><el-input type="textarea" :placeholder="this.course.pos" v-model="this.course.pos"></el-input></el-col>
            </el-row>
            <el-row>
                <el-col class="col1">上课时间</el-col><el-col class="col2"><el-input type="textarea" :placeholder="this.course.times" v-model="this.course.times"></el-input></el-col>
            </el-row>
        </table>
        <br>
        <el-button type="primary" @click="onSubmit">确认</el-button>
    </div>
</template>

<script>
export default {
    mounted () {
        axios.get('http://localhost:8000/courses/'+this.$route.params.id, {}).then(response => (this.course = response.course))
    },
    data () {
        return {
            course : {
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
        }
    }
}
</script>

<style>
  table {
    width: 80%;
    margin: 0px auto;
    box-align: center;
    background-color: azure;
  }
  .el-row{
    margin-bottom: 3%;
  }
  .col1{
    margin-left: 10%;
    width: 10%;
  }
  .col2{
    margin-right: 10%;
    width: 70%;
  }
</style>