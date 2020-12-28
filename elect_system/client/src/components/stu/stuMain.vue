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
        <el-table-column width="450" label="时间">
          <template slot-scope="scope">
              开始时间：
              {{new Date(scope.row.start_time).getFullYear()+'-'+(new Date(scope.row.start_time).getMonth()+1)+'-'+new Date(scope.row.start_time).getDate()+' '+new Date(scope.row.start_time).getHours()+':'+new Date(scope.row.start_time).getMinutes()+':'+new Date(scope.row.start_time).getSeconds()}}
          </template>
        </el-table-column>
        <el-table-column
          prop="theme"
          label="详细时间信息"
          width="360">
        </el-table-column>
        <el-table-column
          prop="detail"
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
    theme: '补推选1',
    detail: '暂无'
  }
]
export default {
  name: 'Main',
  data () {
    return {tableData: Data}
  },
  mounted () {
    axios.get('http://39.98.75.17:8000/phase/phases').then(response => (this.tableData = response.data.data))
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
