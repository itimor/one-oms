<template>
  <div class="app-container">
    <h1>这是一个测试页面</h1>
    <h3>下面是你对这个页面的相关操作权限，如果没有，则不会显示相应的按钮</h3>
    <el-button v-if="permissionList.add" size="small" type="primary">
      {{ "增加" }}
    </el-button>
    
    <el-button v-if="permissionList.del" size="small" type="danger">
      {{ "删除" }}
    </el-button>
    
    <el-button v-if="permissionList.update" size="small" type="warning">
      {{ "编辑" }}
    </el-button>
    
    <el-button v-if="permissionList.view" size="small" type="success">
      {{ "查看" }}
    </el-button>
  </div>
</template>

<script>
  import {requestMenuButton} from '@/api/sys/menu'
  import {checkAuthAdd, checkAuthDel, checkAuthView, checkAuthUpdate} from '@/utils/permission'
  
  export default {
    name: 'test',
    data() {
      return {
        operationList: [],
        permissionList: {
          add: false,
          del: false,
          view: false,
          update: false
        }
      }
    },
    created() {
      this.getMenuButton()
    },
    methods: {
      checkPermission() {
        this.permissionList.add = checkAuthAdd(this.operationList)
        console.log(this.permissionList.add)
        this.permissionList.del = checkAuthDel(this.operationList)
        this.permissionList.view = checkAuthView(this.operationList)
        this.permissionList.update = checkAuthUpdate(this.operationList)
      },
      getMenuButton() {
        requestMenuButton('test').then(response => {
          this.operationList = response.data
        }).then(() => {
          this.checkPermission()
        })
      },
    }
  }
</script>
