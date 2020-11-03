<template>
  <div id="app">
    <el-container>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="1"><a href="/test/hello/" target="_self">处理中心</a></el-menu-item>
      <el-submenu index="2">
        <template slot="title">我的工作台</template>
        <el-menu-item index="2-1"><a href="/main" target="_self">面</a></el-menu-item>
        <el-menu-item index="2-2">选项2</el-menu-item>
        <el-menu-item index="2-3">选项3</el-menu-item>
        <el-submenu index="2-4">
          <template slot="title">选项4</template>
          <el-menu-item index="2-4-1">选项1</el-menu-item>
          <el-menu-item index="2-4-2">选项2</el-menu-item>
          <el-menu-item index="2-4-3">选项3</el-menu-item>
        </el-submenu>
      </el-submenu>
      <el-menu-item index="3" disabled>消息中心</el-menu-item>
      <el-menu-item index="4"><a href="/" target="_self">{{ message }}</a></el-menu-item>
    </el-menu>
    </el-container>
    <el-row>
      <el-input v-model="message"></el-input>
    </el-row>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    var a
    if (this.$route.path == '/main') {
      a = '2-1'
    } else if (this.$route.path == '/') {
      a = '4'
    } else {
      a = '1'
    }
    // alert(a)
    return {
      activeIndex: a,
      message: 'Hello Vue!'
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
