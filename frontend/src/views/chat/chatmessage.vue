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
        >{{ "搜索" }}</el-button>
        <el-button
          v-if="permissionList.del"
          :disabled="multipleSelection.length<1"
          class="filter-item"
          type="danger"
          icon="el-icon-delete"
          @click="handleBatchDel"
        >{{ "删除" }}</el-button>
      </el-button-group>
    </div>

    <el-table
      :data="list"
      v-loading="listLoading"
      border
      style="width: 100%"
      highlight-current-row
      @sort-change="handleSortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column label="群组" prop="group">
        <template slot-scope="{ row }">
          <el-tag type="primary">{{row.group.name}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="创建者" prop="create_user">
        <template slot-scope="{ row }">
          <el-tag type="success">{{row.create_user.realname}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="消息" prop="message"></el-table-column>
      <el-table-column label="创建时间" prop="create_time"></el-table-column>
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
  </div>
</template>

<script>
import { chatmessage, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate
} from "@/utils/permission";

export default {
  name: "chatmessage",

  components: { Pagination },
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
      multipleSelection: []
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
    this.getList();
  },
  methods: {
    checkPermission() {
      this.permissionList.add = checkAuthAdd(this.operationList);
      this.permissionList.del = checkAuthDel(this.operationList);
      this.permissionList.view = checkAuthView(this.operationList);
      this.permissionList.update = checkAuthUpdate(this.operationList);
    },
    getMenuButton() {
      auth
        .requestMenuButton("chatmessage")
        .then(response => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      chatmessage.requestGet(this.listQuery).then(response => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
      });
    },
    handleFilter() {
      this.getList();
    },
    handleSortChange(val) {
      if (val.order === "ascending") {
        this.listQuery.ordering = val.prop;
      } else if (val.order === "descending") {
        this.listQuery.ordering = "-" + val.prop;
      } else {
        this.listQuery.ordering = "";
      }
      this.getList();
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleBatchDel() {
      this.$confirm("是否确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          const ids = this.multipleSelection.map(x => x.id);
          chatmessage.requestBulkDelete(ids).then(response => {
            console.log(response.results);
            this.getList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    }
  }
};
</script>
