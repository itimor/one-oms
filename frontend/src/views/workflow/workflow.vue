<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="请输入内容"
        clearable
        prefix-icon="el-icon-search"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter"
        @clear="handleFilter"
      />
      <el-button-group>
        <el-button
          class="filter-item"
          type="primary"
          icon="el-icon-search"
          @click="handleFilter"
        >
          {{ "搜索" }}
        </el-button>
        <el-button
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
        >
          {{ "添加" }}
        </el-button>
        <el-button
          v-if="permissionList.del"
          class="filter-item"
          type="danger"
          icon="el-icon-delete"
          @click="handleBatchDel"
        >
          {{ "删除" }}
        </el-button>
      </el-button-group>
    </div>
    
    <el-table :data="list" v-loading="listLoading" border style="width: 100%" highlight-current-row @sort-change="handleSortChange"
              @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"/>
      <el-table-column label="名称" prop="name"></el-table-column>
      <el-table-column label="状态" prop="status" sortable="custom">
        <template slot-scope="scope">
          <span>{{scope.row.status}}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="permissionList.update"
              size="small"
              type="primary"
              @click="handleUpdate(row)"
            >
              {{ "编辑" }}
            </el-button>
            <el-button
              v-if="permissionList.del"
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >
              {{ "删除" }}
            </el-button>
            <el-button
              v-if="permissionList.add"
              size="small"
              type="warning"
              @click="handleCreateFlow(row)"
            >
              {{ "编排步骤" }}
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-pagination">
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="listQuery.offset"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="80px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="temp.name"/>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-switch
            v-model="temp.status"
            active-color="#13ce66"
            inactive-color="#ff4949">
          </el-switch>
        </el-form-item>
        <el-form-item label="备注" prop="memo">
          <el-input v-model="temp.memo"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogStepVisible = false">
          {{ "取消" }}
        </el-button>
        <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">
          {{ "确定" }}
        </el-button>
      </div>
    </el-dialog>
    
    <el-dialog title="编排步骤" :visible.sync="dialogFlowVisible">
      <el-steps :active="active">
        <el-step
          v-for="node in steplist"
          :key="node.id"
          :title="node.name"
          :description="node.action_user"
        ></el-step>
      </el-steps>
      <el-divider>
        <i class="el-icon-s-opportunity"></i>
      </el-divider>
      <div class="filter-container">
        <el-button
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleStepCreate"
        >
          {{ "添加" }}
        </el-button>
      </div>
      
      <el-table :data="steplist" border highlight-current-row>
        <el-table-column label="名称" prop="name"></el-table-column>
        <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
          <template slot-scope="{ row }">
            <el-button-group>
              <el-button
                size="small"
                type="primary"
                @click="handleStepUpdate(row)"
              >
                {{ "编辑" }}
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="handleStepDelete(row)"
              >
                {{ "删除" }}
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogStepVisible">
      <el-form
        ref="stepForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="80px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="temp.name"/>
        </el-form-item>
        <el-form-item label="执行者" prop="memo">
          <el-select v-model="temp.action_user" placeholder="请选择用户">
            <el-option v-for="item in users" :key="item.id" :label="item.username" :value="item.username"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="sequence">
          <el-input v-model="temp.sequence"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogStepVisible = false">
          {{ "取消" }}
        </el-button>
        <el-button type="primary" @click="dialogStatus === 'create' ? createStepData() : updateStepData()">
          {{ "确定" }}
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {requestMenuButton} from '@/api/sys/menu'
  import {requestGet, requestPost, requestPut, requestDelete} from '@/api/workflow/workflow'
  import * as step from "@/api/workflow/workflowstep"
  import * as sys from "@/api/sys/user"
  import Pagination from '@/components/Pagination'
  import {checkAuthAdd, checkAuthDel, checkAuthView, checkAuthUpdate} from '@/utils/permission'
  
  export default {
    name: 'workflow',
    components: {Pagination},
    data() {
      return {
        operationList: [],
        permissionList: {
          add: false,
          del: false,
          view: false,
          update: false
        },
        list: [],
        total: 0,
        listLoading: true,
        loading: true,
        listQuery: {
          offset: 1,
          limit: 20,
          search: undefined,
          ordering: undefined
        },
        temp: {},
        dialogFormVisible: false,
        dialogFlowVisible: false,
        dialogStatus: '',
        textMap: {
          update: '编辑',
          create: '添加',
        },
        rules: {
          name: [{required: true, message: '请输入名称', trigger: 'blur'}]
        },
        multipleSelection: [],
        workflow_id: 0,
        active: 1,
        users: [],
        steplist: [],
        steptemp: {},
        dialogStepVisible: false,
      }
    },
    created() {
      this.getMenuButton()
      this.getList()
      this.getUserList()
    },
    methods: {
      checkPermission() {
        this.permissionList.add = checkAuthAdd(this.operationList)
        this.permissionList.del = checkAuthDel(this.operationList)
        this.permissionList.view = checkAuthView(this.operationList)
        this.permissionList.update = checkAuthUpdate(this.operationList)
      },
      getMenuButton() {
        requestMenuButton('user').then(response => {
          this.operationList = response.data
        }).then(() => {
          this.checkPermission()
        })
      },
      getList() {
        this.listLoading = true
        requestGet(this.listQuery).then(response => {
          this.list = response.results
          this.total = response.count
          this.listLoading = false
        })
      },
      getStepList() {
        step.requestGet(this.listQuery).then(response => {
          this.steplist = response.results
        })
      },
      getUserList() {
        sys.requestGet().then(response => {
          this.users = response;
        })
      },
      handleFilter() {
        this.getList()
      },
      handleSortChange(val) {
        if (val.order === 'ascending') {
          this.listQuery.ordering = val.prop
        } else if (val.order === 'descending') {
          this.listQuery.ordering = '-' + val.prop
        } else {
          this.listQuery.ordering = ''
        }
        this.getList()
      },
      resetTemp() {
        this.temp = {
          name: '',
          status: true,
          memo: '',
          action_user: '',
          sequence: 10
        }
      },
      handleCreate() {
        this.resetTemp()
        this.dialogStatus = 'create'
        this.dialogFormVisible = true
        this.loading = false
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      createData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            this.loading = true
            requestPost(this.temp).then(response => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '创建成功',
                type: 'success',
                duration: 2000
              })
              this.getList()
            }).catch(() => {
              this.loading = false
            })
          }
        })
      },
      handleUpdate(row) {
        this.temp = row
        this.dialogStatus = 'update'
        this.dialogFormVisible = true
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      updateData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            this.loading = true
            requestPut(this.temp.id, this.temp).then(() => {
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '更新成功',
                type: 'success',
                duration: 2000
              })
              this.getList()
            }).catch(() => {
              this.loading = false
            })
          }
        })
      },
      handleDelete(row) {
        this.$confirm('是否确定删除?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          requestDelete(row.id).then(() => {
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.getList()
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      },
      handleSelectionChange(val) {
        this.multipleSelection = val
      },
      handleBatchDel() {
        if (this.multipleSelection.length === 0) {
          this.$message({
            message: '未选中任何行',
            type: 'warning',
            duration: 2000
          })
          return
        }
        this.$confirm('是否确定删除?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          for (const v of this.multipleSelection) {
            requestDelete(v).then(() => {
              this.getList()
            })
          }
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      },
      handleCreateFlow(row) {
        this.dialogFlowVisible = true
        this.workflow_id = row.id
        this.getStepList()
      },
      handleStepCreate() {
        this.resetTemp()
        this.dialogStatus = 'create'
        this.dialogStepVisible = true
        this.$nextTick(() => {
          this.$refs['stepForm'].clearValidate()
        })
      },
      createStepData() {
        this.$refs['stepForm'].validate((valid) => {
          if (valid) {
            step.requestPost(this.temp).then(response => {
              this.dialogStepVisible = false
              this.$notify({
                title: '成功',
                message: '创建成功',
                type: 'success',
                duration: 2000
              })
              this.getStepList()
            }).catch(() => {
              this.loading = false
            })
          }
        })
      },
      handleStepUpdate(row) {
        this.temp = row
        this.dialogStatus = 'update'
        this.dialogStepVisible = true
        this.$nextTick(() => {
          this.$refs['stepForm'].clearValidate()
        })
      },
      updateStepData() {
        this.$refs['stepForm'].validate((valid) => {
          if (valid) {
            step.requestPut(this.temp.id, this.temp).then(() => {
              this.dialogStepVisible = false
              this.$notify({
                title: '成功',
                message: '更新成功',
                type: 'success',
                duration: 2000
              })
              this.getStepList()
            }).catch(() => {
            })
          }
        })
      },
      handleStepDelete(row) {
        this.$confirm('是否确定删除?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          console.log(row)
          step.requestDelete(row.id).then(() => {
            this.$message({
              message: '删除成功',
              type: 'success'
            })
            this.getStepList()
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
      }
    }
  }
</script>
