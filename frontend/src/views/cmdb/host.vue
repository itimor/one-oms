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
          v-if="permissionList.add"
          class="filter-item"
          type="success"
          icon="el-icon-edit"
          @click="handleCreate"
        >{{ "添加" }}</el-button>
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
    >
      <el-table-column label="名称" prop="hostname"></el-table-column>
      <el-table-column label="主IP" prop="ip"></el-table-column>
      <el-table-column label="主机组" prop="groups">
        <template slot-scope="{ row }">
          <span v-for="item in row.groups" :key="item.id">{{item.name}}</span>
        </template>
      </el-table-column>
      <el-table-column label="机房" prop="idc">
        <template slot-scope="{ row }">
          <span>{{row.idc.name}}</span>
        </template>
      </el-table-column>
      <el-table-column label="类型" prop="asset_type">
        <template slot-scope="{ row }">
          <span>{{row.asset_type|ASSET_TYPEFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" prop="status">
        <template slot-scope="{ row }">
          <span>{{row.asset_type|ASSET_STATUSFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column label="系统" prop="os"></el-table-column>
      <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
        <template slot-scope="{ row }">
          <el-button-group>
            <el-button
              v-if="permissionList.update"
              size="small"
              type="primary"
              @click="handleUpdate(row)"
            >{{ "编辑" }}</el-button>
            <el-button
              v-if="permissionList.del"
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >{{ "删除" }}</el-button>
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
    <el-dialog
      :title="textMap[dialogStatus]"
      :visible.sync="dialogFormVisible"
      :close-on-click-modal="false"
    >
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="80px"
        style="width: 400px; margin-left:50px;"
      >
        <el-form-item label="名称" prop="hostname">
          <el-input v-model="temp.hostname" />
        </el-form-item>
        <el-form-item label="ip" prop="ip">
          <el-input v-model="temp.ip" />
        </el-form-item>
        <el-form-item label="主机组" prop="groups">
          <el-select v-model="temp.groups" filterable multiple placeholder="请选择主机组">
            <el-option
              v-for="item in group_list"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="机房" prop="idc">
          <el-select v-model="temp.idc" filterable placeholder="请选择机房">
            <el-option v-for="item in idc_list" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="类型" prop="asset_type">
          <el-select v-model="temp.asset_type" filterable placeholder="请选择设备类型">
            <el-option
              v-for="(label, value) in ASSET_TYPE"
              :key="value"
              :label="label"
              :value="value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="temp.status" filterable placeholder="请选择设备状态">
            <el-option
              v-for="(label, value) in ASSET_STATUS"
              :key="value"
              :label="label"
              :value="value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="资产编号" prop="an">
          <el-input v-model="temp.an" />
        </el-form-item>
        <el-form-item label="系统" prop="os">
          <el-input v-model="temp.os" />
        </el-form-item>
        <el-form-item label="备注" prop="memo">
          <el-input v-model="temp.memo" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">{{ "取消" }}</el-button>
        <el-button
          type="primary"
          @click="dialogStatus === 'create' ? createData() : updateData()"
        >{{ "确定" }}</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { host, idc, hostgroup, auth } from "@/api/all";
import Pagination from "@/components/Pagination";
import {
  checkAuthAdd,
  checkAuthDel,
  checkAuthView,
  checkAuthUpdate,
} from "@/utils/permission";

export default {
  name: "host",

  components: { Pagination },
  data() {
    return {
      operationList: [],
      permissionList: {
        add: false,
        del: false,
        view: false,
        update: false,
      },
      list: [],
      total: 0,
      listLoading: true,
      loading: true,
      listQuery: {
        offset: 1,
        limit: 20,
        search: undefined,
        ordering: undefined,
      },
      multipleSelection: [],
      temp: {},
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "编辑",
        create: "添加",
      },
      rules: {
        hostname: [{ required: true, message: "请输入名称", trigger: "blur" }],
        ip: [{ required: true, message: "请输入ip", trigger: "blur" }],
        an: [{ required: true, message: "请输入内容", trigger: "blur" }],
        groups: [{ required: true, message: "请输入内容", trigger: "change" }],
        idc: [{ required: true, message: "请输入内容", trigger: "change" }],
        asset_type: [
          { required: true, message: "请输入内容", trigger: "blur" },
        ],
        status: [{ required: true, message: "请输入内容", trigger: "blur" }],
      },
      group_list: [],
      idc_list: [],
      ASSET_STATUS: {
        1: "使用中",
        2: "未使用",
        3: "故障",
        4: "报废",
      },
      ASSET_TYPE: {
        1: "物理机",
        2: "虚拟机",
        3: "容器",
        4: "网络设备",
        5: "其他设备",
      },
    };
  },
  computed: {},
  created() {
    this.getMenuButton();
    this.getList();
    this.getGroupList();
    this.getIdcList();
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
        .requestMenuButton("host")
        .then((response) => {
          this.operationList = response.results;
        })
        .then(() => {
          this.checkPermission();
        });
    },
    getList() {
      this.listLoading = true;
      host.requestGet(this.listQuery).then((response) => {
        this.list = response.results;
        this.total = response.count;
        this.listLoading = false;
      });
    },
    getGroupList() {
      hostgroup.requestGet().then((response) => {
        this.group_list = response.results;
      });
    },
    getIdcList() {
      idc.requestGet().then((response) => {
        this.idc_list = response.results;
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
    resetTemp() {
      this.temp = {
        hostname: "",
        ip: "",
        groups: [],
        idc: "",
        asset_type: "",
        status: "",
        an: "",
        os: "",
        memo: "",
      };
    },
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.dialogFormVisible = true;
      this.loading = false;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          this.loading = true;
          host
            .requestPost(this.temp)
            .then((response) => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "创建成功",
                type: "success",
                duration: 2000,
              });
              this.temp.id = response.data.id;
              this.list.unshift(this.temp);
            })
            .catch(() => {
              this.loading = false;
            });
        }
      });
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row, {
        idc: row.idc.id,
        groups: row.groups.map((a) => a.id),
      });
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          this.loading = true;
          host
            .requestPut(this.temp.id, this.temp)
            .then(() => {
              this.dialogFormVisible = false;
              this.$notify({
                title: "成功",
                message: "更新成功",
                type: "success",
                duration: 2000,
              });
            })
            .catch(() => {
              this.loading = false;
            });
        }
      });
    },
    handleDelete(row) {
      this.$confirm("是否确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          host.requestDelete(row.id).then(() => {
            this.$message({
              message: "删除成功",
              type: "success",
            });
            this.getList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleBatchDel() {
      this.$confirm("是否确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          const ids = this.multipleSelection.map((x) => x.id);
          chatmessage.requestBulkDelete(ids).then((response) => {
            console.log(response.results);
            this.getList();
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
  },
};
</script>
