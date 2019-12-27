<template>
  <div class="app-container">
    <div class="filter-container">
      <div class="ticket">
        <el-card>
          <div slot="header">
            <a class="tickettitle">{{ticketData.name}}</a>
            <hr class="heng"/>

            <div class="appendInfo">
              <table class="viewticket">
                <tbody>
                <tr>
                  <td>工单号</td>
                  <td>{{ ticketData.pid }}</td>
                  <td>创建者</td>
                  <td>{{ ticketData.create_user }}</td>
                </tr>
                <tr>
                  <td>工单类型</td>
                  <td>{{ ticketData.workflow }}</td>
                  <td>创建时间</td>
                  <td>{{ ticketData.create_time | parseDate }}</td>
                </tr>
                <tr>
                  <td>流程状态</td>
                  <td>
                    <el-steps :active="ticketData.step" finish-status="success" process-status="finish" simple>
                      <el-step v-for="item in steps" :title="item.name"></el-step>
                    </el-steps>
                  </td>
                  <td>操作</td>
                  <td>
                    <el-button v-if="ticketData.status<4" type="primary">转交下一步</el-button>
                    <el-button type="warning">驳回工单</el-button>
                    <el-button v-if="username===ticketData.create_user" type="danger">关闭工单</el-button>
                  </td>
                </tr>
                </tbody>
              </table>
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

          <!--<div class="ticketenclosure">-->
          <!--<ul>-->
          <!--<li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">-->
          <!--<i class="fa fa-paperclip"></i>-->
          <!--<a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>-->
          <!--<el-button type="text" icon="el-icon-delete"-->
          <!--@click="deleteEnclosure(item.id)"></el-button>-->
          <!--</li>-->
          <!--</ul>-->
          <!--</div>-->
        </el-card>

        <el-card class="issue">
          <div class="editor-container">
            <markdown-editor v-model="commentForm.content"/>
          </div>
          <div class="editor-button">
            <el-button type="primary" @click="submitForm">提交</el-button>
          </div>
        </el-card>


        <el-card>
          工单回复
          <hr class="heng"/>
          <ul v-for="item in replys" :key="item.id" class="am-comments-list am-comments-list-flip">
            <li class="am-comment">
              <el-avatar class="am-comment-avatar">{{item.create_user | AvatarFilter }}</el-avatar>
              <div class="am-comment-main">
                <header class="am-comment-hd">
                  <div class="am-comment-meta">
                    <a class="am-comment-author">{{item.create_user}}</a>
                    回复于
                    <time :datetime="item.create_time">{{item.create_time|parseDate}}</time>
                  </div>
                </header>

                <div class="am-comment-bd">
                  <vue-markdown :source="item.content"></vue-markdown>
                </div>
              </div>
            </li>
          </ul>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
  import {requestMenuButton} from '@/api/sys/menu'
  import {requestGet, requestPut} from '@/api/workflow/ticket'
  import * as workflowstep from '@/api/workflow/workflowstep'
  import * as ticketreplay from '@/api/workflow/ticketreplay'
  import * as user from '@/api/sys/user'
  import {checkAuthAdd, checkAuthDel, checkAuthView, checkAuthUpdate} from '@/utils/permission'
  import {mapGetters} from 'vuex'
  import MarkdownEditor from '@/components/MarkdownEditor'
  import VueMarkdown from 'vue-markdown' // 前端解析markdown

  export default {
    name: 'viewworkflow',
    components: {MarkdownEditor, VueMarkdown},
    data() {
      return {
        operationList: [],
        permissionList: {
          add: false,
          del: false,
          view: false,
          update: false
        },
        listLoading: true,
        loading: true,
        ticket: '',
        workflows: [],
        ticketData: {},
        steps: [],
        commentForm: {},
        replys: [],
        users: []
      }
    },
    computed: {
      ...mapGetters([
        'username'
      ]),
      UserAvatarFilter() {
        return function (username) {
          this.users.filter(user => {
            console.log(user.username)
            if (user.username === username) {
              console.log(user.avatar)
              return user.avatar
            }
          })
        }
      }
    },
    created() {
      this.ticket = this.$route.params && this.$route.params.id
      this.fetchData()
      this.getMenuButton()
      this.getTicketReplyList()
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
      fetchData() {
        this.listLoading = true
        const query = {
          id: this.ticket
        }
        requestGet(query).then(response => {
          this.ticketData = response[0]
          this.commentForm = {
            ticket: this.ticketData.id,
            create_user: this.username
          }
          this.getWorkflowStepList(this.ticketData.workflow)
          this.listLoading = false
        })
      },
      getWorkflowStepList(workflow) {
        const query = {
          workflow: workflow
        }
        workflowstep.requestGet(query).then(response => {
          this.steps = response
        })
      },
      getUserList() {
        user.requestGet().then(response => {
          this.users = response
        })
      },
      resetTemp() {
        this.commentForm = {
          ticket: this.ticketData.id,
          create_user: this.username,
          content: ''
        }
      },
      getTicketReplyList() {
        const query = {
          ticket: this.ticket
        }
        ticketreplay.requestGet(query).then(response => {
          this.replys = response
        })
      },
      submitForm() {
        ticketreplay.requestPost(this.commentForm).then(response => {
          this.dialogFormVisible = false
          this.$notify({
            title: '成功',
            message: '创建成功',
            type: 'success',
            duration: 2000
          })
          this.resetTemp()
          this.getTicketReplyList()
        }).catch(() => {
          this.loading = false
        })
      }
    }
  }
</script>

<style lang="scss">
  .tickettitle {
    color: #0a76a4;
    font-size: 24px;
  }

  .viewticket {
    width: 100%;
    tr {
      td {
        padding: 10px;
        &:nth-child(odd) {
          background: #a5b9f1;
          width: 150px;
        }
        &:nth-child(even) {
          background: #cccccc;
          width: 300px;
        }
      }
    }
  }

  .ticket {
    margin: 0 20px;
    .issue {
      margin: 20px 0;
      padding: 10px;
      .editor-container {
        padding-bottom: 10px;
      }
      .editor-button {
        float: right;
      }
    }
  }

</style>
