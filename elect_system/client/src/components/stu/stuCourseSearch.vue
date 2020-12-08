<template>
<el-main>
    <el-form :inline="true" :model="formInline" class="form-inline">
    <el-form-item label="课程名称">
        <el-input v-model="formInline.name" placeholder="课程名称"></el-input>
    </el-form-item>
    <el-form-item label="院系">
        <el-select v-model="formInline.region" placeholder="活动区域">
        <el-option v-for=" (name,nameIndex) in this.department" :key="nameIndex" :label="name" :value="name"></el-option>
        </el-select>
    </el-form-item>
    <el-form-item>
        <el-button type="primary" @click="onSubmit">查询</el-button>
    </el-form-item>
    </el-form>
    <el-row v-if="this.OnSearch===true">
        <el-pagination
            background
            layout="prev, pager, next"
            :total="1000">
        </el-pagination>
    </el-row>
</el-main>
</template>
<script>
export default {
  data () {
    return {
      formInline: {
        name: '',
        region: ''
      },
      OnSearch: false,
      department: ['信科', '不是信科']
    }
  },
  mounted () {
    this.OnSearch = false
  },
  methods: {
    onSubmit () {
      console.log('submit!')
      this.OnSearch = true
    }
  }
}
</script>
