<template>
  <div>
    <el-form ref="loginForm" :model="form" :rules="rules" label-width="80px" class="login-box">
      <h2 class="login-title">学生登录系统</h2>
      <h3 class="login-title">欢迎登录</h3>
      <el-form-item label="账号" prop="username">
        <el-input type="text" placeholder="请输入账号" v-model="form.username"/>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" placeholder="请输入密码" v-model="form.password"/>
      </el-form-item>
      <el-form-item>
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
import {setCookie,getCookie} from '../../assets/js/cookies.js'
import axios from 'axios'
export default {
  name: 'Login',
  mounted(){
  /*页面挂载获取cookie，如果存在username的cookie，且前五位是admin，则跳转到主页，不需登录*/
    if(getCookie('username').substring(0,3)=="stu"){
        this.$router.push('/stuMain')
    }
  },
  data () {
    return {
      form: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          {required: true, message: '账号不可为空', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '密码不可为空', trigger: 'blur'}
        ]
      },
      dialogVisible: false
    }
  },
  methods: {
    stuLogin () {
        if(this.username == "" || this.password == ""){
            alert("请输入用户名或密码")
        }else{
            let data = {'username':this.username,'password':this.password}
            /*接口请求*/
            axios.post('http://localhost:8000/stu/Login',this.form,{withCredentials:true}).then((res)=>{
                console.log(res)
              if(res.code == 404){
                  this.tishi = "该用户不存在"
                  this.showTishi = true
              }else if(res.data == -200){
                  this.tishi = "密码输入错误"
                  this.showTishi = true
              }else if(res.data == 200){
                  this.tishi = "登录成功"
                  this.showTishi = true
                  setCookie('username','stu'+this.username,1000*60)
                  setTimeout(function(){
                      this.$router.push('/stuMain')
                  }.bind(this),1000)
              }
          })
      }
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
