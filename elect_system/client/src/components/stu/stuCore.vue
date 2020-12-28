<template>
    <div>
      <el-row>
          <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
                <el-menu-item index="1"><el-link :underline="false" href='\stuMain'>主界面</el-link></el-menu-item>
                <el-menu-item index="2"><el-link :underline="false" href='\stuPersonal'>我的课程</el-link></el-menu-item>
                <el-menu-item index="3"><el-link :underline="false" href='\stuCourseSearch'>课程搜索</el-link></el-menu-item>
                <el-menu-item index="4"><el-link :underline="false" href='\stuProgram'>培养方案</el-link></el-menu-item>
          </el-menu>
      </el-row>
            <el-badge class='divcss5-a'>
              <el-button size="small" type="info" v-on:click="logout()">登出</el-button>
            </el-badge>
             <el-badge :value="infonum" :hidden="hidden" class='divcss5-b'>
              <el-popover
                placement="bottom"
                title="消息内容"
                width="600"
                trigger="click"
                >
                <el-button size="small" slot="reference">消息</el-button>
                  <el-table :data="messages">
                    <el-table-column width="150" label="消息标题" property="title"></el-table-column>
                    <el-table-column width="450" label="消息时间" property="time">
                      <template slot-scope="scope">
                          <el-button type="text" @click="noteread(scope.$index)">{{new Date(scope.row.time)}}</el-button>
                      </template>
                    </el-table-column>
                  </el-table>
              </el-popover>
            </el-badge>
            <div class="line"></div>
        <router-view></router-view>
    </div>
</template>
<script>
import axios from 'axios'
import {getCookie,delCookie} from '../../assets/js/cookies.js'
export default {
  data () {
    let res = 1
    if (this.$route.path === '/stuMain') {
      res = 1
    } else if (this.$route.path === '/stuPersonal') {
      res = 2
    } else if (this.$route.path === '/stuCourseSearch') {
      res = 3
    } else if (this.$route.path === '/stuProgram') {
      res = 4
    }
    return {
      infonum: 1,
      hidden: (this.infonum <= 0),
      activeIndex: res.toString(),
      messages: [
        {
          'id': 2,
          'title': '选课消息',
          'time': 1600012345000,
          'content': '抽签已结束，您成功选中的课程：xxx、yyy，未选中的课程：yyy',
          'hasRead': false
        }]
    }
  },
  methods: {
    mounted () {
      if (getCookie('username').substring(0, 3) !== 'stu') {
        alert('学生登录失效')
        this.$router.push('/stuLogin')
      }
      axios.get('http://39.98.75.17:8000/user/login', {withCredentials: true}).then((res) => {
        return res.data
      }).then(data => {
        if (data.success !== true) {
          alert('获取消息失败')
        } else {
          this.messages = data.messages
          this.infonum = data.unReadNum
        }
      })
    },
    logout () {
      axios.post('http://39.98.75.17:8000/user/logout', {withCredentials: true}).then((res) => {
        delCookie('username')
        this.$router.push('/stuLogin')
      })
    },
    noteread (index) {
      let message = this.messages[index]
      this.$alert(message.content)
      if (message.hasRead === false) {
        axios.post('http://39.98.75.17:8000/user/message' + message.id.toString(), {withCredentials: true}).then((res) => {
        })
        this.messages[index].hasRead = true
        this.infonum--
        this.hidden = (this.infonum <= 0)
      }
      console.log(this.hidden)
    }
  }
}
</script>
<style scoped>
.divcss5-a{position:absolute;right:40px;top:20px}
.divcss5-b{position:absolute;right:120px;top:20px}
.el-menu-demo{margin-left:30px;margin-right:30px}
</style>
