<template>
    <div>
        <v-row>{{course.name}}</v-row>
        <v-row>
            <v-col>课程ID</v-col><v-col><el-input type="textarea" :placeholder="course.course_id" v-model="course.course_id"></el-input></v-col>
        </v-row>
        <v-row>
            <v-col>班号</v-col><v-col><el-input type="textarea" :placeholder="course.class_no" v-model="course.class_no"></el-input></v-col>
        </v-row>
        <v-row>
            <v-col>学分</v-col><v-col><el-input type="textarea" :placeholder="course.credit" v-model="course.credit"></el-input></v-col>
        </v-row>
        <v-row>
            <v-col>开课院系</v-col><v-col><el-input type="textarea" :placeholder="course.dept" v-model="course.dept"></el-input></v-col>
        </v-row>
        <v-row>
            <v-col>任课老师</v-col><v-col><el-input type="textarea" :placeholder="course.lecturer" v-model="course.lecturer"></el-input></v-col>
        </v-row>
        <v-row>
            <v-col>上课地点</v-col><v-col><el-input type="textarea" :placeholder="course.pos" v-model="course.pos"></el-input></v-col>
        </v-row>
        <v-row>
            <v-col>上课时间</v-col><v-col><el-input type="textarea" :placeholder="course.times" v-model="course.times"></el-input></v-col>
        </v-row>
        <el-button type="primary" ></el-button>
    </div>
</template>

<script>
export default {
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