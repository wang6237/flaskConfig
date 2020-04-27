<template>
    <div>
      <div>
        <!--<h3 style="width: 100px;">用户列表</h3>-->
        <!--<div style="width: 200px;margin-right: 500px">-->
          <el-button class="el-button" type="primary" style="margin: 10px; margin-left: 90%;" @click="addUser">添加用户</el-button>
        <!--</div>-->
      </div>
      <!--<el-table-header>用户列表</el-table-header>-->
      <el-table
      :key="tableKey"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"

      >
        <el-table-column label="ID" prop="id" sortable="custom" align="center" width="200">
          <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Username" align="center" >
          <template slot-scope="scope">
            <span>{{ scope.row.username }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Password" align="center" show-password>
          <template slot-scope="scope">
            <span show-password >{{ scope.row.password }}</span >
          </template>
        </el-table-column>
        <el-table-column label="Role" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.role }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Email" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.email }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Actions" align="center">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="handleUpdate(row)">
              Edit
            </el-button>
            <el-button type="primary" size="mini" @click="handleDelete(row)">
              Delete
            </el-button>
          </template>
        </el-table-column>

      </el-table>


      <el-dialog :title="textMap[dialogStatus]" :visible.sync="addUserFormVisible">
        <el-form ref="addUserDataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
          <!--<el-form-item label="用户名" prop="username">-->
          <el-form-item label="用户名" >
            <el-input v-model="temp.username" v-bind:disabled="isUsernameDisabled" >


            </el-input>

          </el-form-item>

          <!--<el-form-item label="密码" prop="password" >-->
          <el-form-item label="密码"  >
            <el-input v-model="temp.password" placeholder="请输入密码"  show-password>

            </el-input>

          </el-form-item>
          <!--<el-form-item label="Email" prop="email">-->
          <el-form-item label="Email" >
            <el-input v-model="temp.email">

            </el-input>

          </el-form-item>
          <!--<el-form-item label="Role" prop="role">-->
          <el-form-item label="Role" >
            <el-select v-model="temp.role" class="filter-item" placeholder="Please select">
              <el-option v-for="item in roleTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
        <el-button @click="resetTemp()">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createDate():updateDate()">
          Confirm
        </el-button>
      </div>
      </el-dialog>



    </div>
</template>

<script>
  // import ElTableHeader from "element-ui/packages/table/src/table-header";
  // import ElTableBody from "element-ui/packages/table/src/table-body";
  import { getUserListInfo,createUser,updateUser, deleteUser } from "@/api/user";
  const roleTypeOptions = [
    { key: 'guest', display_name: 'Guest' },
    { key: 'admin', display_name: 'Admin' },
    { key: 'dev', display_name: 'Dev' },
    { key: 'test', display_name: 'Test' }
  ]
  export default {
    name: "userList",
    // components: {ElTableBody, ElTableHeader},
    data(){
      return {
        list:[],
        total: '',
        tableKey: 0,
        listLoading: true,
        addUserFormVisible: false,
        isUsernameDisabled : false,
        roleTypeOptions,
        temp: {
          username: '',
          password: '',
          role: '',
          email: ''
        },
        textMap: {
          update: 'Edit',
          create: '添加用户'
        },
        dialogStatus: '',
        rules: {
          username: [{ required: true, message: 'username is required', trigger: 'blur' }],
          password: [{ required: true, message: 'password is required', trigger: 'change' }],
          email: [{ required: true, message: 'email is required', trigger: 'change' }],
          roles: [{ required: true, message: 'role is required', trigger: 'change' }],
        },
      }
    },
    created() {
      this.getUserInfo()
    },
    methods: {
      getUserInfo(){
        // this.listLoading = true;
        getUserListInfo().then(response => {
          console.log(response.data);
          this.list = response.data.items;
          this.total = response.data.total

        } )

      },
      addUser(){
        this.dialogStatus = 'create'
        this.addUserFormVisible = true

      },
      createDate() {
        this.$refs['addUserDataForm'].validate((valid) => {
          if (valid) {
            // this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
            // this.temp.author = 'vue-element-admin'
            createUser(this.temp).then(res => {
              // console.log(res.data)
              const msg = res.data.msg
              // this.list.unshift(this.temp)
              this.addUserFormVisible = false;
              this.$notify({
                title: 'Success',
                message: msg,
                type: 'success',
                duration: 2000
              });
              this.getUserInfo();
              this.resetTemp()
            })
          }
        })
      },
      updateDate() {
        this.$refs['addUserDataForm'].validate((valid) => {
          if (valid) {
            const tempData = Object.assign({}, this.temp)
            // tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
            updateUser(tempData).then(() => {
              // for (const v of this.list) {
              //   if (v.id === this.temp.id) {
              //     const index = this.list.indexOf(v)
              //     this.list.splice(index, 1, this.temp)
              //     break
              //   }
              // }
              this.addUserDataForm = false;
              this.$notify({
                title: 'Success',
                message: 'Update Successfully',
                type: 'success',
                duration: 2000
              });
              this.getUserInfo();
              this.addUserFormVisible = false;
              this.resetTemp()
            })
          }
        })
      },
      handleUpdate(row) {
        this.temp = Object.assign({}, row); // copy obj
        // this.temp.timestamp = new Date(this.temp.timestamp)
        this.dialogStatus = 'update';
        this.addUserFormVisible = true;
        this.isUsernameDisabled = true;
        // const v = this.add_username;
        // this.temp.username = row.name;
        // this.temp.email = row.email;
        // this.temp.role = row.roles;
        // '#add_username'.disabled = true;
        // const v = this.$refs['#add_username'];

        // console.log(row)
        // console.log(this.has_disabled)

        // console.log(this.temp)
        // this.temp.username = row.username;
        // this.temp.email = row.email;
        // this.temp.role = row.role
        // this.$nextTick(() => {
        //   this.$refs['addUserDataForm'].clearValidate()
        // })
      },
      handleDelete(row) {
        this.temp = Object.assign({}, row);
        const username = this.temp.username
        deleteUser(username).then(res => {
          console.log(res);
          this.getUserInfo();
          this.$notify({
                title: 'Success',
                message: 'Delete User Successfully',
                type: 'success',
                duration: 2000
              });
        })


      },
      resetTemp() {
        this.addUserFormVisible = false
        this.isUsernameDisabled = false
        this.temp = {
          username: '',
          password: '',
          role: '',
          email: ''
        }
      }
    }
  }
</script>

<style scoped>

</style>
