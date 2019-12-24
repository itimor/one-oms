<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="workticket">
        <el-card>
          <div slot="header" class="clearfix">
            <a class="title">{{ticketData.name}}</a>
            <hr class="heng"/>

            <div class="appendInfo">
              <a class="ticketinfo create_user"><span class="han">
                                工单创建时间：</span>{{ticketData.create_time | parseDate}}</a>
              <a class="ticketinfo create_user"><span class="han">
                              <a class="shu"></a>
                                工单发起人：</span>{{ticketData.create_user}}</a>
              <a class="ticketinfo action_user"><span class="han">
                              <a class="shu"></a>
                               工单指派者：</span>{{ticketData.action_user}}</a>
              <a class="ticketinfo action_user" v-if="ticketData.ticket_status!=0">
                <a class="shu"></a>
                <span class="han">最新回复人：</span>{{ticketData.edit_user}}</a>
              <a class="shu"></a>
              <span class="han">工单类型：</span>
              <a>{{ticketData.type}}</a>
              <a class="shu"></a>
              <span class="han">工单当前状态：</span>
              <el-tag :type="STATUS_TYPE[ticketData.ticket_status]">
                {{STATUS_TEXT[ticketData.ticket_status]}}
              </el-tag>
            </div>
            <div class="appendInfo" v-if="ticketData.ticket_status!=2">
              <span class="han">工单操作：</span>
              <el-button v-if="role==='super'&&ticketData.ticket_status===0" type="success" size="small"
                         @click="changeStatus">接收
              </el-button>
              <div class="action">
                <el-radio-group v-model="radio_status">
                  <el-radio label="0">不操作</el-radio>
                  <el-radio label="2">关闭工单</el-radio>
                  <el-radio v-if="role==='super'" label="1">更改指派人</el-radio>
                </el-radio-group>
                <div class="action" v-if="radio_status==1">
                  <el-select v-model="rowdata.action_user" filterable placeholder="请选择指派人">
                    <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
                  </el-select>
                </div>
              </div>

            </div>
          </div>

          <vue-markdown :source="ticketData.content"></vue-markdown>

          <div v-if="ticketData.ticket_status<2">
            <hr class="heng"/>
            <el-upload
              ref="upload"
              :action="uploadurl"
              :on-success="handleSuccess"
              :show-file-list="false">
              <el-button slot="trigger" size="mini" type="danger" plain icon="upload2" :disabled="count>2">
                上传附件
              </el-button>
              <div slot="tip" class="el-upload__tip">
                <p>上传文件不超过10m，<a style="color: red">最多只能上传3个文件</a></p>
              </div>
            </el-upload>
            <hr class="heng"/>
          </div>

          <div v-if='enclosureData.length>0' class="ticketenclosure">
            <ul>
              <li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">
                <i class="fa fa-paperclip"></i>
                <a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>
                <el-button type="text" icon="el-icon-delete"
                           @click="deleteEnclosure(item.id)"></el-button>
              </li>
            </ul>
          </div>
        </el-card>
      </div>

      <div v-if="ticketData.ticket_status<2">
        <el-form :model="commentForm" ref="mailcontent" label-width="80px">
          <hr class="heng"/>
          <el-form-item label="问题处理" prop="content">
            <mavon-editor style="z-index: 1" v-model="mailcontent" code_style="monokai" :toolbars="toolbars"
                          @imgAdd="imgAdd" ref="md"></mavon-editor>
            <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到问题处理里面</a>
          </el-form-item>
          <el-form-item v-if="radio_status === '0'" label="通知人" prop="action_user">
            <el-select v-model="ticketData.create_user" filterable placeholder="请选择通知人">
              <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
            </el-select>
            <el-checkbox v-model="sendnotice">发送通知</el-checkbox>
          </el-form-item>
          <el-form-item v-if="radio_status === '0'" label="通知运维">
            <el-checkbox v-model="sendop"></el-checkbox>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-card class="ticketcomment" v-if="commentData.length>0">
        处理历史记录
        <div v-for="item in commentData" :key="item.id">
          <hr class="heng"/>
          <el-row>
            <el-col :span="1">
              <el-button type="primary" plain class="commentuser">{{item.create_user}}</el-button>
            </el-col>
            <el-col :span="20">
              <div class="dialog-box">
                <span class="bot"></span>
                <span class="top"></span>
                <div class="comment">
                  <vue-markdown :source="item.content"></vue-markdown>
                  <p class="commenttime">处理时间：{{item.create_time | parseDate}}</p>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </el-card>
  </div>
</template>

<script>
  import {requestMenuButton} from '@/api/sys/menu'
  import {requestGet, requestPut} from '@/api/workflow/ticket'
  import * as ticketreplay from '@/api/workflow/ticketreplay'
  import {checkAuthAdd, checkAuthDel, checkAuthView, checkAuthUpdate} from '@/utils/permission'
  import {mapGetters} from 'vuex'

  export default {
    name: 'viewworkflow',
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
        workflows: []
      }
    },
    computed: {
      ...mapGetters([
        'username'
      ])
    },
    created() {
      this.getMenuButton()
      this.getList()
      this.getWorkflowList()
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
      getWorkflowList() {
        workflow.requestGet().then(response => {
          this.workflows = response
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
          workflow: '',
          name: '',
          content: '',
          create_user: ''
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
      changeWorkflow(val) {
        this.temp.pid = getConversionTime('pid')
        this.temp.name = val + '-' + getConversionTime()
        this.temp.create_user = this.username
      }
    }
  }
</script>
