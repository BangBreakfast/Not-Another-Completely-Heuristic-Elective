<template>
  <div>
    <el-form ref="course" :model="course" label-width="auto" :rules="rules">
      <el-row>
        <h1>{{course.name}}</h1>
      </el-row>
      <el-row justify="center" type="flex">
        <el-col span="4">
          <el-form-item label="课程ID" prop="course_id">
            <el-input v-model.number="course.course_id"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row justify="center" type="flex">
        <el-col span="4">
          <el-form-item label="班号" prop="class_no">
            <el-input v-model.number="course.class_no"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row justify="center" type="flex">
        <el-col span="4">
          <el-form-item label="学分" prop="credit">
            <el-input v-model.number="course.credit"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row justify="center" type="flex">
        <el-col span="4">
          <el-form-item label="开课院系" prop="dept">
            <el-input v-model.number="course.dept"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row justify="center" type="flex">
        <el-col span="4">
          <el-form-item label="任课老师" prop="lecturer">
            <el-input v-model="course.lecturer"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row justify="center" type="flex">
        <el-col span="4">
          <el-form-item label="上课地点" prop="pos">
            <el-input v-model="course.pos"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row justify="center" type="flex">
        <el-col span="4">
          <el-form-item label="课程ID" prop="course_id">
            <el-input v-model.number="course.course_id"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item>
        <el-button type="primary" @click="submitForm('course')">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  mounted() {
    axios
      .get("http://localhost:8000/courses/" + this.$route.params.id, {})
      .then(response => (this.course = response.course));
  },
  data() {
    return {
      course: {
        course_id: 1233343,
        class_no: 1,
        name: "软件工程",
        credit: 4,
        times: [
          { day: 2, period: [3, 4] },
          { day: 4, period: [5, 6] }
        ],
        time: "周二吃早饭",
        lecturer: "孙艳春",
        pos: "理教201",
        dept: 48,
        election: {
          status: 1,
          willpoint: 99,
          elected_num: 121,
          capacity: 150,
          pending_num: 13
        }
      },
      rules: {
        course_id: [
          { required: true, message: "请输入课程ID", trigger: "blur" },
          { type: "number", message: "请输入数字", trigger: "blur" }
        ],
        class_no: [
          { required: true, message: "请输入班号", trigger: "blur" },
          { type: "number", message: "请输入数字", trigger: "blur" }
        ],
        credit: [
          { required: true, message: "请输入学分", trigger: "blur" },
          { type: "number", message: "请输入数字", trigger: "blur" }
        ],
        dept: [
          { required: true, message: "请输入院系", trigger: "blur" },
          { type: "number", message: "请输入数字", trigger: "blur" }
        ],
        lecturer: [
          { required: true, message: "请输入任课教师", trigger: "blur" }
        ],
        pos: [{ required: true, message: "请输入上课地点", trigger: "blur" }],
        times: {}
      },
      methods: {
        submitForm(formName) {
          axios.post('http://localhost:8000/courses/' + this.$route.params.id, this.course, {withCredentials: true});
        }
      }
    };
  }
};
</script>

<style>
table {
  width: 80%;
  margin: 0px auto;
  box-align: center;
  background-color: azure;
}
.col1 {
  margin-left: 10%;
  width: 10%;
}
.col2 {
  margin-right: 10%;
  width: 70%;
}
</style>