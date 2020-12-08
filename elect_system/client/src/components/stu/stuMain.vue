<template>
    <div>
      <el-main>
        <el-row :gutter="20">
        <el-col :span="3"><div class="grid-content bg-purple"></div></el-col>
        <el-col :span="18">
        <el-table
        :data="tableData"
        border
        style="width: 100%">
        <el-table-column
          prop="date"
          label="时间类型"
          width="180">
        </el-table-column>
        <el-table-column
          prop="detail"
          label="详细时间信息"
          width="360">
        </el-table-column>
        <el-table-column
          prop="info"
          label="备注">
        </el-table-column>
        </el-table>
        </el-col>
        <el-col :span="3"><div class="grid-content bg-purple"></div></el-col>
        </el-row>
            <el-divider></el-divider>
        <el-row style="border-radius: 2px box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)">
          还没有注意事项哦！
        </el-row>
      </el-main>
    </div>
</template>

<script>
import axios from 'axios'
let Data = [
  {
    date: '昨天',
    detail: '暂无',
    info: '嗝'
  }
]
export default {
  name: 'Main',
  data () {
    return {tableData: Data}
  },
  mounted () {
    axios.get('http://localhost:8000/time/timetable.json').then(response => (this.Data = response))
      .catch(function (error) { // 请求失败处理
        console.log(error)
      })
  }
}
</script>

<style scoped>
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
</style>
