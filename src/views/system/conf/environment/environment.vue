<template>
  <div class="app-container">
    <div class="dashboard-text">环境列表</div>
    <div>
      <el-button
        class="el-button"
        type="primary"
        style="margin: 10px; margin-left: 90%;"
        @click="add"
      >添加</el-button>
    </div>
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      style="width: 100%;"
    >
      <el-table-column type="expand">
        <template slot-scope="scope">
          <SyncEtcd
            :config-info="scope.row.content"
            :env-id="scope.row.id"
            @reload="reload"
          />
        </template>
      </el-table-column>
      <el-table-column label="ID" prop="id" sortable="custom" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="名称" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="路径" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.path }}</span>
        </template>
      </el-table-column>
      <el-table-column label="备注" class-name="status-col">
        <template slot-scope="scope">
          <span>{{ scope.row.comment }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row.id)"
          >
            删除
          </el-button>
          <el-button
            size="mini"
            type="primary"
            @click="handleGetList(scope.row)"
          >
            编辑
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total > 0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList"
    />
    <el-dialog title="增加环境" :visible.sync="addEnvFormVisible">
      <el-form
        ref="envDataForm"
        :rules="rules"
        :model="env"
        label-position="left"
        label-width="110px"
        style="width: 600px; margin-left:50px;"
      >
        <el-form-item label="名称">
          <el-input
            v-model="env.name"
            placeholder="请输入环境名称， 确保唯一"
          />
        </el-form-item>
        <el-form-item label="Path">
          <el-input
            v-model="env.path"
            placeholder="请输入etcd中的path，绝对path"
          />
        </el-form-item>
        <el-form-item label="模板">
          <el-select
            v-model="templateSelect"
            multiple
            placeholder="请选择模板"
            style="width: 100%"
          >
            <el-option
              v-for="item in templateOption"
              :key="item.id"
              :label="item.name"
              :value="item.name"
            />
          </el-select>
        </el-form-item>
        <!--        <el-form-item label="Etcd Server">-->
        <!--          <el-select v-model=" etcdServerSelect"    placeholder="请选择模板" style="width: 100%">-->
        <!--            <el-option v-for="item in etcdServerOption" :key="item.id" :label="item.name+' => '+ item.info" :value="item.info"/>-->
        <!--          </el-select>-->
        <!--        </el-form-item>-->
        <el-form-item label="备注">
          <el-input v-model="env.comment" type="textarea" placeholder="备注" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addEnvFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="createDate()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
    <el-dialog title="查看环境" :visible.sync="editEnvFormVisible" width="80%">
      <el-form
        ref="envDataForm"
        :rules="rules"
        :model="env"
        label-position="left"
        label-width="110px"
        style="width: 90%; margin-left:50px;"
      >
        <el-form-item label="名称">
          <el-input
            v-model="env.name"
            placeholder="请输入环境名称， 确保唯一"
          />
        </el-form-item>
        <el-form-item label="Path">
          <el-input
            v-model="env.path"
            disabled
            placeholder="请输入etcd中的path，绝对path"
          />
        </el-form-item>
        <el-form-item label="模板">
          <el-select
            v-model="templateSelect"
            multiple
            placeholder="请选择模板"
            style="width: 100%"
          >
            <el-option
              v-for="item in templateOption"
              :key="item.id"
              :label="item.name"
              :value="item.name"
              :disabled="item.disabled"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="env.comment" type="textarea" placeholder="备注" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editEnvFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="editDate()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import {
  getEnvLists,
  addEnvList,
  editEnvList,
  delEnvList
} from '@/api/getEnvironment'
import { getTemplateList } from '@/api/getTemplateApi'
// eslint-disable-next-line no-unused-vars
// import { getEtcdServerList } from '@/api/getConfigApi'
// import Templ from '../templ/index'
import SyncEtcd from './syncEtcd'

export default {
  name: 'Env',
  components: { Pagination, SyncEtcd },
  directives: {},
  filters: {},
  data() {
    return {
      isText: 'Welcome env pages',
      tableKey: 0,
      listLoading: true,
      list: [],
      total: 0,
      items: [],
      listQuery: {
        page: 1,
        limit: 10,
        sort: '+id'
      },
      env: {
        id: 0,
        name: '',
        path: '',
        template_name: [],
        content: '',
        comment: '',
        etcd_ip: ''
      },
      templateList: {
        items: [],
        total: 0
      },
      templateOption: [],
      templateSelect: [],
      // etcdServerOption: [],
      // etcdServerSelect: [],
      addEnvFormVisible: false,
      editEnvFormVisible: false,
      // contentData: [],
      hasDisable: true,
      configInfo: [],
      envId: 0,
      rules: {
        // name: [{ required: true, message: 'type is required', trigger: 'change' }],
        type: [
          { required: true, message: 'type is required', trigger: 'change' }
        ],
        timestamp: [
          {
            type: 'date',
            required: true,
            message: 'timestamp is required',
            trigger: 'change'
          }
        ],
        name: [
          { required: true, message: 'title is required', trigger: 'blur' }
        ]
      },
      activeNames: []
    }
  },
  mounted() {},
  created() {
    this.getList()
    this.getEnvData()
  },
  methods: {
    getList() {
      this.listLoading = true
      // const { page, limit } = this.listQuery
      getEnvLists().then(response => {
        this.list = response.data.items
        this.total = response.data.total
        // console.log(this.list)
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    resetEnv() {
      this.env = {
        id: 0,
        name: '',
        path: '',
        template_name: [],
        content: '',
        comment: '',
        etcd_ip: ''
      }
      this.templateSelect = []
      // console.log(val);
    },
    getEnvData() {
      getTemplateList().then(response => {
        // console.log("getEnvData",response.data)
        this.templateOption = response.data.items
        // this.templateList['total'] = response.data.total
      })
      // getEtcdServerList().then(response => {
      //   this.etcdServerOption =response.data.items
      // })
    },
    add() {
      this.addEnvFormVisible = true
      // this.getEnvData()
      console.log(this.templateSelect, this.etcdServerSelect)
    },
    createDate() {
      console.log(this.templateSelect, this.etcdServerSelect)
      this.env.template_name = this.templateSelect
      // this.env.etcd_ip = this.etcdServerSelect
      // console.log(this.env.content)
      // addEnvList(env)
      this.$refs['envDataForm'].validate(valid => {
        if (valid) {
          // this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          // this.temp.author = 'vue-element-admin'
          addEnvList(this.env).then(res => {
            // console.log(res.data)
            const msg = res.data.msg
            const type = res.data.type
            // this.list.unshift(this.temp)
            this.addEnvFormVisible = false
            this.$notify({
              title: 'Success',
              message: msg,
              type: type,
              duration: 2000
            })
            this.resetEnv()

            this.getList()
            this.getEnvData()
            this.$nextTick(() => {
              this.$refs['envDataForm'].clearValidate()
            })
          })
        }
      })
    },
    handleGetList(row) {
      // this.contentData = row.content
      this.env = row
      for (const t in this.env.content) {
        for (const i in this.templateOption) {
          if (this.env.content[t].name === this.templateOption[i].name) {
            this.templateOption[i].disabled = true
          }
        }
      }
      this.editEnvFormVisible = true
    },
    handleDelete(id) {
      delEnvList(id).then(res => {
        const msg = res.data.msg
        const type = res.data.type
        // this.list.unshift(this.temp)
        // this.addEnvFormVisible = false;
        this.$notify({
          title: 'Success',
          message: msg,
          type: type,
          duration: 2000
        })

        this.getList()
        this.getEnvData()
      })
    },
    reload(data) {
      // console.log(data)
      this.getList()
      this.getEnvData()
    },
    editDate() {
      console.log(this.env)
      console.log(this.templateSelect)
      this.env.template_name = this.templateSelect
      this.$refs['envDataForm'].validate(valid => {
        if (valid) {
          // this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          // this.temp.author = 'vue-element-admin'
          let id = this.env.id
          editEnvList(id,this.env).then(res => {
            // console.log(res.data)
            const msg = res.data.msg
            const type = res.data.type
            // this.list.unshift(this.temp)
            this.editEnvFormVisible = false
            this.$notify({
              title: 'Success',
              message: msg,
              type: type,
              duration: 2000
            })
            this.resetEnv()
            this.getList()
            this.getEnvData()
            this.$nextTick(() => {
              this.$refs['envDataForm'].clearValidate()
            })
          })
        }
      })

      // console.log('>>>>>>>')
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
