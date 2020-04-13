<template>
  <div>
    <el-form label-position="left" >
      <el-table
      :data="configInfo"
      style="width: 100%">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-input   type="textarea" autosize v-model="props.row.content" ></el-input>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="模板名称"
        prop="name">
      </el-table-column>
      <el-table-column
        label="路径"
        prop="path">
      </el-table-column>
      <el-table-column
        label="是否与etcd数据是否一致"
        prop="state">

      </el-table-column>
      <el-table-column label="操作" align="center"  class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button size="mini" type="danger" @click="handleSyncEtcdDelete(scope.row, envId)"> 删除 </el-button>
          <el-button size="mini" type="primary" @click="handleSyncEtcd(scope.row)"> 同步 </el-button>
          <el-button size="mini"  @click="handleComparison(scope.row.content, scope.row.etcdData)"> 对比 </el-button>


        </template>
      </el-table-column>
    </el-table>
    </el-form>

    <el-dialog :visible.sync="comparisonVisible" width="80%">
      <el-table :data="comparisonData">
        <el-table-column label="数据库中的数据" prop="db">
          <template slot-scope="scope">
            <el-input   type="textarea" autosize v-model="scope.row.db" disabled></el-input>
          </template>

        </el-table-column>
        <el-table-column label="etcd Server中的数据" prop="etcd">
          <template slot-scope="scope">
            <el-input   type="textarea" autosize v-model="scope.row.etcd" disabled></el-input>
          </template>

        </el-table-column>
      </el-table>

<!--      <el-divider direction="vertical"></el-divider>-->

<!--      <el-divider direction="vertical"></el-divider>-->

    </el-dialog>
  </div>
</template>

<script>
  import {  syncEtcd, syncEtcdDelete, syncState } from '@/api/getEnvironment'
  export default {
    name: 'sync',
    components: {},
    props: ['configInfo', 'envId'],
    data(){
      return {
        isHidden: false,
        comparisonVisible: false,
        comparisonData:
          [{
            'db': '',
            'etcd': ''
          }],
      }
    },
    created() {
      this.intervalid1 = setInterval(() => {
      // 根据porjectSelected的值，刷新stack信息
        this.refresh()
      }, 5000)
    },
    methods: {
      handleSyncEtcd(row){
        console.log(row)
        syncEtcd(row).then(res => {
          const msg = res.data.msg
          const type = res.data.type
          this.$notify({
            title: 'Success',
            message: msg,
            type: type,
            duration: 2000
          });
        })
      },
      handleSyncEtcdDelete: function(row, envId) {
        const path = row.path

        // console.log(envId)
        syncEtcdDelete(path, envId).then(res => {
          const msg = res.data.msg
          const type = res.data.type
          this.$notify({
            title: 'Success',
            message: msg,
            type: type,
            duration: 2000
          })
          this.$emit("reload", '刷新页面')
        })
      },
      refresh(){
        console.log(this.configInfo, 'refresh>>>>>>')
        for (let i in this.configInfo){
          const postData = {
            'path': this.configInfo[i]['path'],
            'content': this.configInfo[i]['content'],
            'envId': this.envId
          }
          syncState(postData).then(res => {
            // console.log(res.data.state)
            const state = res.data.state
            const items = res.data.items
            // this.configInfo[i]['state'] = state
            if (state === 1){
              this.configInfo[i]['state'] = '数据不一致'
              this.configInfo[i]['etcdData'] = items
              // console.log(this.configInfo[i]['etcdData'])
            }else {
              this.configInfo[i]['state'] = '数据一致'
              this.configInfo[i]['etcdData'] = items
            }
          })
        }
      },
      handleComparison(dbData, etcdDate){
        this.comparisonVisible = true
        this.comparisonData[0].db = dbData
        this.comparisonData[0].etcd = etcdDate
        console.log('com',this.comparisonData)

      }
    },
    beforeDestroy() {
      clearInterval(this.intervalid1)
    }
  }

</script>
