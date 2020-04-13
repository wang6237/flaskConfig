<template>
  <div class="app-container">
    <div class="dashboard-text">etcd 信息</div>
    <div>
        <!--<h3 style="width: 100px;">用户列表</h3>-->
        <!--<div style="width: 200px;margin-right: 500px">-->
          <el-button class="el-button" type="primary" style="margin: 10px; margin-left: 90%;" @click="addEtcdS">添加 etcd</el-button>
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
      <el-table-column label="名称"  align="center" >
        <template slot-scope="scope">
          <span >{{ scope.row.name }} </span>
        </template>
      </el-table-column>
      <el-table-column label="相关信息" class-name="status-col">
        <template slot-scope="scope">
          <!--<el-tag :type="row.state ">-->
            {{ scope.row.info }}
          <!--</el-tag>-->
        </template>
      </el-table-column>
      <el-table-column label="备注" class-name="status-col" >
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
      <el-table-column label="操作" align="center" width="330" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button  size="mini" type="danger" @click="handleDelete(row)">
            删除
          </el-button>
          <el-button  size="mini" type="success" @click="handleGetList(row)">
            编辑
          </el-button>
<!--          <el-button  size="mini" type="Warning" @click="handleWaitList(row)">-->
<!--            待接收-->
<!--          </el-button>-->
        </template>
      </el-table-column>


    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog title="增加 etcd" :visible.sync="addEtcdFormVisible">
      <el-form ref="addEtcdDataForm" :rules="rules" :model="temp" label-position="left" label-width="110px" style="width: 600px; margin-left:50px;">
        <!--<el-form-item label="用户名" prop="username">-->
        <el-form-item label="etcd 名称：" >
          <el-input v-model="temp.name" placeholder="请输入etcd名称, 确保唯一"  >
          </el-input>

        </el-form-item>

        <!--<el-form-item label="密码" prop="password" >-->
        <!--<el-form-item label="Control URL："  >-->
          <!--<el-input v-model="temp.control_url" placeholder="请输入Control的URL" >-->

          <!--</el-input>-->

        <!--</el-form-item>-->
        <el-form-item label="etcd info："  >
          <el-input type="textarea" v-model="temp.info" placeholder="请输入etcd的信息，ip:port 使用分号分隔" >

          </el-input>

        </el-form-item>
<!--        <el-form-item label="Control PORT："  >-->
<!--          <el-input v-model="temp.port" placeholder="请输入Control的PORT" >-->

<!--          </el-input>-->

<!--        </el-form-item>-->
        <el-form-item label="备注"  >
          <el-input v-model="temp.comment" placeholder="备注" >

          </el-input>

        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addEtcdFormVisible = false">
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
// import { fetchList, fetchPv, createArticle, updateArticle } from '@/api/article'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { getEtcdServerList, addEtcd, deleteEtcd,getetcd,getEtcdAction,addEtcdServer } from '@/api/getConfigApi'


export default {
  name: 'control',
  components: { Pagination },
  directives: { waves },
  // filters: {
  //   sizeFilter(size) {
  //     console.log(size)
  //     // const statusMap = {
  //     //   healthy: 'success',
  //     //   degraded: 'warning',
  //     //   unhealthy: 'danger'
  //     // }
  //     return size/1024
  //   },
  //   typeFilter(type) {
  //     return calendarTypeKeyValue[type]
  //   },
  //   stateFilter(state) {
  //     const statusMap = {
  //       active: 'success',
  //       degraded: 'warning',
  //       inactive: 'danger',
  //       upgraded: '#409EFF'
  //     }
  //     return statusMap[state]
  //   },
  //
  // },
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
        info: ''
      },
      // waittemp: {
      //   ip: '',
      //   port: '',
      //   name: ''
      // },
      // listTagQuery: {
      //   name: '',
      //   page: 1,
      //   limit: 10,
      //   sort: '+id'
      // },
      // hasStatusDisable: false,
      // controlInfoList: [],
      // controlWaitList: [],
      // ControlTitle: '',
      // projectOptions: [],
      // porjectSelected: '',
      // tagslist: [],
      // tagstotal: 0,
      addEtcdFormVisible: false,
      // ControlFormVisible: false,
      // ControlWaitFormVisible: false,
      // dialogStatus: '',
      // textMap: {
      //   update: 'Edit',
      //   create: 'Create'
      // },
      rules: {
        type: [{ required: true, message: 'type is required', trigger: 'change' }],
        timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList();
    // this.getListStack()
  },
  methods: {
    getList(){
      // console.log()
      this.listLoading = true

      const {page, limit } = this.listQuery
      // console.log(page,limit);
      getEtcdServerList(page,limit).then(response => {
        this.list = response.data.items;
        this.total = response.data.total;
        console.log(this.list)
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })

    },
    handleDelete(row){
      // const name = row
      // console.log(name.control_name)
      const name = row.name
      deleteEtcd(name).then(res => {
        const msg = res.data.msg
        const type = res.data.type
        // this.list.unshift(this.temp)
        // this.addProjectFormVisible = false;
        this.$notify({
          title: 'Success',
          message: msg,
          type: type,
          duration: 2000
        });
        this.getList();
      });


    },
    // handleGetList(row){
    //   const ip = row.ip
    //   const port = row.port
    //   const action = 'GetList'
    //   // const name =
    //   getControl(ip,port,action).then(res => {
    //     this.controlInfoList = res.data.items
    //     this.ControlFormVisible = true
    //     this.ControlTitle = row.control_name+' 已接收的列表'
    //   });
    // },
    // handleRemove(row){
    //   // const ip = row.ip
    //   // const port = row.port
    //   console.log(row)
    //   // console.log(event.target.getAttribute('stop'))
    //   this.rpcTemp.control_name = this.ControlTitle.split(' ')[0]
    //   this.rpcTemp.rpc_ip = row.ip
    //   this.rpcTemp.rpc_name = row.name
    //   this.rpcTemp.action = 'Remove'
    //   getControlAction(this.rpcTemp).then(res => {
    //     const msg = res.data.msg
    //     const type = res.data.type
    //     this.$notify({
    //       title: 'Success',
    //       message: msg,
    //       type: type,
    //       duration: 2000
    //     });
    //     this.ControlFormVisible = false
    //   });
    // },
    // handleAccept(row){
    //   // const ip = row.ip
    //   // const port = row.port
    //   this.rpcTemp.control_name = this.ControlTitle.split(' ')[0]
    //   this.rpcTemp.rpc_ip = row.ip
    //   this.rpcTemp.rpc_name = row.name
    //   this.rpcTemp.action = 'Accept'
    //   console.log(this.rpcTemp.control_name)
    //   getControlAction(this.rpcTemp).then(res => {
    //     const msg = res.data.msg
    //     const type = res.data.type
    //     this.$notify({
    //       title: 'Success',
    //       message: msg,
    //       type: type,
    //       duration: 2000
    //     });
    //     // this.ControlWaitFormVisible = false
    //     const action = 'GetWaitList'
    //     getControl(this.waittemp.ip,this.waittemp.port,action).then(res => {
    //       this.controlWaitList = res.data.items
    //       // this.ControlWaitFormVisible = true
    //       this.ControlTitle = this.waittemp.name+' 等待接收的列表'
    //     });
    //   });
    //
    //
    // },
    // handleStop(row){
    //   // const ip = row.ip
    //   // const port = row.port
    //   this.rpcTemp.control_name = this.ControlTitle.split(' ')[0]
    //   this.rpcTemp.rpc_ip = row.ip
    //   this.rpcTemp.rpc_name = row.name
    //   this.rpcTemp.rpc_port = row.port
    //   this.rpcTemp.action = 'Stop'
    //   getControlAction(this.rpcTemp).then(res => {
    //     console.log(res)
    //     const msg = res.data.msg
    //     const type = res.data.type
    //     this.$notify({
    //       title: 'Success',
    //       message: msg,
    //       type: type,
    //       duration: 2000
    //     });
    //   });
    // },
    // handleWaitList(row){
    //   this.waittemp.ip = row.ip
    //   this.waittemp.port = row.port
    //   this.waittemp.name = row.control_name
    //   const action = 'GetWaitList'
    //   // const name =
    //   getControl(this.waittemp.ip,this.waittemp.port,action).then(res => {
    //     this.controlWaitList = res.data.items
    //     this.ControlWaitFormVisible = true
    //     this.ControlTitle = this.waittemp.name+' 等待接收的列表'
    //   });
    // },
    // handleGetTags(row) {
    //   this.temp = Object.assign({}, row)
    //   this.listTagQuery.name =  this.temp.name
    //   this.dialogFormVisible = true;
    //   this.getTagsList()
    // },

    // handleFilter() {
    //   this.listQuery.page = 1
    //   this.getAppsList()
    // },
    addEtcdS(){
      this.addEtcdFormVisible = true
      this.resetTemp()

    },
    resetTemp() {
      this.temp = {
        name: '',
        comment: '',
        info: ''
      }
    },

    createDate() {

      this.$refs['addEtcdDataForm'].validate((valid) => {
        if (valid) {
          // this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          // this.temp.author = 'vue-element-admin'
          addEtcdServer(this.temp).then(res => {
            // console.log(res.data)
            const msg = res.data.msg
            const type = res.data.type
            // this.list.unshift(this.temp)
            this.addEtcdFormVisible = false;
            this.$notify({
              title: 'Success',
              message: msg,
              type: type,
              duration: 2000
            });

            this.getList();
            this.$nextTick(() => {
              this.$refs["addEtcdDataForm"].clearValidate();
            });
          })
        }
      })
    },

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
