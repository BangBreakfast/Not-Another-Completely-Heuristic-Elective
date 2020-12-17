<template>
  <div>
    <el-form ref="loginForm" :model="form" :rules="rules" label-width="80px" class="login-box">
      <h2 class="login-title">添加学生</h2>
      <el-form-item label="账号" prop="uid">
        <el-input type="text" placeholder="请输入账号" v-model="form.uid"/>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" placeholder="请输入密码" v-model="form.password"/>
      </el-form-item>
      <el-form-item>
        <el-button v-on:click="link()">切换到教务系统</el-button>
        <el-button type="primary" v-on:click="stuLogin()">登录</el-button>
      </el-form-item>
    </el-form>
    <el-dialog
      title="温馨提示"
      :visible.sync="showTishi"
      width="30%"
      :before-close="handleClose">
      <span>{{tishi}}</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="showTishi = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    return {
      form: {
        uid: '',
        name: '吃饭',
        gender: true,         // True=male, False=female
        dept: 48,
        grade: 2017,
        credit_limit: 30,      // Default is 25
        password: ''
      },
      rules: {
        uid: [
          {required: true, message: '账号不可为空', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '密码不可为空', trigger: 'blur'}
        ]
      },
      tishi: '',
      showTishi: false,
      success: ''
    }
  },
  methods: {
    stuLogin () {
      if (this.uid === '' || this.password === '') {
        alert('请输入用户名或密码')
      } else {
        /* 接口请求 */
        axios.post('http://localhost:8000/user/students', {students: [this.form]}, {withCredentials: true}).then((res) => {
          console.log(res)
          res = res.data
          // cookie = res.headers
          if (res.success === false) {
            this.tishi = '注册失败'
            this.showTishi = true
          } else if (res.success === true) {
            this.success = 'true'
            this.tishi = '添加成功'
            this.showTishi = true
            setTimeout(function () {
              this.$router.push('/stuMain')
            }.bind(this), 1000)
          }
        })
      }
    },
    link () {
      this.$router.push('/adminLogin')
    }
  }
}
</script>

<style lang="scss" scoped>
  .login-box {
    border: 1px solid #DCDFE6;
    width: 350px;
    margin: 180px auto;
    padding: 35px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }

  .login-title {
    text-align: center;
    margin: 0 auto 40px auto;
    color: #303133;
  }
</style>
