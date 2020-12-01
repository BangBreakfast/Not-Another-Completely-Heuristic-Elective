<template>
    <div>
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="1"><el-link :underline="false" href='\adminMain'>主界面</el-link></el-menu-item>
            <el-menu-item index="2"><el-link :underline="false" href='\adminManual'>手动选课</el-link></el-menu-item>
            <el-menu-item index="3"><el-link :underline="false" href='\adminCourseSearch'>课程搜索</el-link></el-menu-item>
            <el-menu-item index="4"><el-link :underline="false" href='\adminProgram'>培养方案</el-link></el-menu-item>
            <el-menu-item index="5"><el-link :underline="false" href='\adminTime'>修改抽签时间</el-link></el-menu-item>
            </el-menu>
            <div class="line"></div>
        <router-view></router-view>
    </div>
</template>
<script>
import {getCookie} from '../../assets/js/cookies.js'
export default {
  data () {
    let res = 1
    if (this.$route.path === '/adminMain') {
      res = 1
    } else if (this.$route.path === '/adminManual') {
      res = 2
    } else if (this.$route.path === '/adminCourseSearch') {
      res = 3
    } else if (this.$route.path === '/adminProgram') {
      res = 4
    } else if (this.$route.path === '/adminTime') {
      res = 5
    } return {
      activeIndex: res.toString()
    }
  },
  mounted () {
    if (getCookie('username').substring(0, 5) !== 'admin') {
      this.$router.push('/adminLogin')
    }
  }
}
</script>
<style lang="postcss" scoped>

</style>
