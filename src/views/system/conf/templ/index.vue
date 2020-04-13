<template>
  <div class="app-container">
    <div class="dashboard-text">模板列表</div>
    <div>
      <!--<h3 style="width: 100px;">用户列表</h3>-->
      <!--<div style="width: 200px;margin-right: 500px">-->
      <el-button class="el-button" type="primary" style="margin: 10px; margin-left: 90%;" @click="addTemplate">添加服务模板</el-button>
      <!--</div>-->
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="100">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="名称" align="center" width="150">
        <template slot-scope="scope">
          <span>{{ scope.row.name }} </span>
        </template>
      </el-table-column>
      <el-table-column label="相关信息" class-name="status-col">
        <template slot-scope="scope">
          <!--<el-tag :type="row.state ">-->
          {{ scope.row.content }}
          <!--</el-tag>-->
        </template>
      </el-table-column>
      <el-table-column label="路径" class-name="status-col" width="200px">
        <template slot-scope="scope">
          <!--<el-tag :type="row.state ">-->
          {{ scope.row.path }}
          <!--</el-tag>-->
        </template>
      </el-table-column>
      <el-table-column label="备注" class-name="status-col" width="150">
        <template slot-scope="scope">
          <!--<el-tag :type="row.state ">-->
          {{ scope.row.comment }}
          <!--</el-tag>-->
        </template>
      </el-table-column>
      <!--<el-table-column label="最近活跃时间"  align="center">-->
      <!--<template slot-scope="scope">-->
      <!--<span>{{ scope.row.project_info.last_activity_at }}</span>-->
      <!--</template>-->
      <!--</el-table-column>-->
      <el-table-column label="操作" align="center" width="150" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button size="mini" type="danger" @click="handleDelete(row)">
            删除
          </el-button>
          <el-button size="mini" type="success" @click="handleGetList(row)">
            编辑
          </el-button>
          <!--          <el-button  size="mini" type="Warning" @click="handleWaitList(row)">-->
          <!--            待接收-->
          <!--          </el-button>-->
        </template>
      </el-table-column>

    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog title="增加 服务模板" :visible.sync="addTemplateFormVisible">
      <el-form ref="templateDataForm" :rules="rules" :model="temp" label-position="left" label-width="110px" style="width: 600px; margin-left:50px;">
        <!--<el-form-item label="用户名" prop="username">-->
        <el-form-item label="模板 名称：" prop="name">
          <el-input v-model="temp.name" placeholder="请输入模板名称, 确保唯一" :disabled="temp.disabled" />
        </el-form-item>
        <el-form-item label="路径：" prop="path">
          <el-input v-model="temp.path" placeholder="请填写存入etcd的路径，即 Key" :disabled="temp.disabled" />
        </el-form-item>
        <el-form-item label="内容：" prop="content">
          <el-input v-model="temp.content" type="textarea" placeholder="请输入模板内容，即 Value" size="Large" />
        </el-form-item>
        <el-form-item label="备注" prop="comment">
          <el-input v-model="temp.comment" placeholder="备注" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addTemplateFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="createDate()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>

import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { getTemplateList, editTemplate, deleteTemplate, addTemplate } from '@/api/getTemplateApi'

export default {
  name: 'Templ',
  components: { Pagination },
  // directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: [],
      total: 0,
      listLoading: true,
      controltableKey: 0,
      listQuery: {
        page: 1,
        limit: 10,
        sort: '+id'
      },
      temp: {
        name: '',
        comment: '',
        content: '',
        path: '',
        disabled: false
      },
      addTemplateFormVisible: false,
      rules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        path: [
          { required: true, message: '请输入在etcd中相对路径', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入模板内容', trigger: 'blur' },
          { min: 1, max: 2048, message: '长度在 1 到 2048 个字符', trigger: 'blur' }
        ],
        comment: [
          { required: false, message: '请输入活动名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
    // this.getListStack()
  },
  methods: {
    getList() {
      // console.log()
      this.listLoading = true

      const { page, limit } = this.listQuery
      getTemplateList().then(response => {
        this.list = response.data.items
        this.total = response.data.total
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleDelete(row) {
      const id = row.id
      deleteTemplate(id).then(res => {
        const msg = res.data.msg
        const type = res.data.type
        // this.list.unshift(this.temp)
        // this.addProjectFormVisible = false;
        this.$notify({
          title: 'Success',
          message: msg,
          type: type,
          duration: 2000
        })
        this.getList()
      })
    },
    handleGetList(row) {
      this.temp.name = row.name
      this.temp.content = row.content
      this.temp.path = row.path
      this.temp.comment = row.comment
      this.temp.disabled = true
      this.temp.id = row.id
      // const action = 'GetList'
      this.addTemplateFormVisible = true
    },

    addTemplate() {
      this.addTemplateFormVisible = true
      this.resetTemp()
    },
    resetTemp() {
      this.temp = {
        name: '',
        comment: '',
        content: '',
        path: '',
        id: 0,
        disabled: false
      }
    },

    createDate() {
      this.$refs['templateDataForm'].validate((valid) => {
        if (valid) {
          if (this.temp.disabled) {
            editTemplate(this.temp.id, this.temp).then(res => {
              const msg = res.data.msg
              const type = res.data.type
              this.addTemplateFormVisible = false
              this.$notify({
                title: 'Success',
                message: msg,
                type: type,
                duration: 2000
              })
              this.getList()
              this.$nextTick(() => {
                this.$refs['templateDataForm'].clearValidate()
              })
            })
          } else {
            addTemplate(this.temp).then(res => {
            // console.log(res.data)
              const msg = res.data.msg
              const type = res.data.type
              // this.list.unshift(this.temp)
              this.addTemplateFormVisible = false
              this.$notify({
                title: 'Success',
                message: msg,
                type: type,
                duration: 2000
              })

              this.getList()
              this.$nextTick(() => {
                this.$refs['templateDataForm'].clearValidate()
              })
            })
          }
        }
      })
    }

  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
