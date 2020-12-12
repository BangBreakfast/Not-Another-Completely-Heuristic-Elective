<template>
    <div>
        <el-row type="flex" justify="center">
          <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
              <el-menu-item index="1"><el-link :underline="false" href='\stuMain'>主界面</el-link></el-menu-item>
              <el-menu-item index="2"><el-link :underline="false" href='\stuPersonal'>我的课程</el-link></el-menu-item>
              <el-menu-item index="3"><el-link :underline="false" href='\stuCourseSearch'>课程搜索</el-link></el-menu-item>
              <el-menu-item index="4"><el-link :underline="false" href='\stuProgram'>培养方案</el-link></el-menu-item>
            </el-menu>
        </el-row>
            <div class="line"></div>
        <router-view></router-view>
    </div>
</template>
<script>
import {getCookie} from '../../assets/js/cookies.js'
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
      activeIndex: res.toString()
    }
  },
  // mounted () {
  //   if (getCookie('username').substring(0, 3) !== 'stu') {
  //     this.$router.push('/stuLogin')
  //   }
  // }
}
</script>
<style scoped>
</style>
