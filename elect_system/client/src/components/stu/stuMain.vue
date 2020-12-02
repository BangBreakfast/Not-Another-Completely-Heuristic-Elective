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
          prop="name"
          label="详细时间信息"
          width="360">
        </el-table-column>
        <el-table-column
          prop="address"
          label="备注">
        </el-table-column>
        </el-table>
        </el-col>
        <el-col :span="3"><div class="grid-content bg-purple"></div></el-col>
        </el-row>
      </el-main>
    </div>
</template>

<script>
export default {
  name: 'Main'
}
</script>

<style scoped>
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
</style>
