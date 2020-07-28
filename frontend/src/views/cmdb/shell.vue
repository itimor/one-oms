<template>
  <div class="app-container">
    <div class="cmd-container">
      <el-row :gutter="20">
        <el-col :span="18">
          <div class="text" ref="list_message">
            <div class="emoji">
              <span>[root@localhost ~]#</span>
              <input type="text" v-model="temp.cmd" @keyup="onKeyup" placeholder="输入命令" />
            </div>
            <p v-for="item in results" :key="item">{{item}}</p>
          </div>
        </el-col>
        <el-col :span="6">
          <ul class="infinite-list">
            <li
              v-for="item in history_list"
              :key="item.id"
              class="infinite-list-item"
              @click="changeCdm(item.cmd)"
            >
              <a>{{ item.cmd }}</a>
            </li>
          </ul>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { history } from "@/api/all";
import { mapGetters } from "vuex";

export default {
  name: "shell",

  components: {},
  data() {
    return {
      listQuery: {
        search: "",
        join_user: "",
        group: undefined,
      },
      temp: {
        cmd: "ping www.baidu.com",
      },
      ws_uri: "/ws/shell/", // ws path
      lockReconnect: false, // 连接失败不进行重连
      maxReconnect: 5, // 最大重连次数，若连接失败
      socket: null,
      results: [],
      history_list: [],
      hostory_listQuery: {
        offset: 1,
        limit: 10,
      },
    };
  },
  computed: {
    ...mapGetters(["user_id"]),
  },
  created() {
    this.getList();
  },
  methods: {
    getList() {
      history.requestGet().then((response) => {
        this.history_list = response.results;
      });
    },
    changeCdm(val) {
      this.temp.cmd = val;
    },
    scrollToBottom() {
      //  在页面加载时让信息滚动到最下面
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs.list_message.scrollTop = this.$refs.list_message.scrollHeight;
        }, 0);
      });
    },
    // 按回车发送信息
    onKeyup(e) {
      if (e.keyCode === 13) {
        this.cmdrun();
      }
    },
    cmdrun() {
      const date = new Date();
      const m =
        date.getMinutes() + 1 < 10
          ? "0" + date.getMinutes()
          : date.getMinutes();
      const s =
        date.getSeconds() + 1 < 10
          ? "0" + date.getSeconds()
          : date.getSeconds();
      const ms =
        date.getMilliseconds().toString().length < 3
          ? "0" + date.getMilliseconds()
          : date.getMilliseconds();
      const groupname = m + "-" + s + "-" + ms;
      this.results = [];
      this.initWebSocket(groupname);
    },
    reconnect() {
      console.log("尝试重连");
      if (this.lockReconnect || this.maxReconnect <= 0) {
        return;
      }
      setTimeout(() => {
        // this.maxReconnect-- // 不做限制
        this.initWebSocket();
      }, 60 * 1000);
    },
    initWebSocket(groupname) {
      //初始化weosocket
      try {
        if ("WebSocket" in window) {
          const ws_scheme =
            window.location.protocol == "https:" ? "wss://" : "ws://";
          const ws_host =
            process.env.NODE_ENV === "development"
              ? "127.0.0.1:8000"
              : window.location.host;
          const ws_url = ws_scheme + ws_host + this.ws_uri + groupname;
          console.log(ws_url);
          this.socket = new WebSocket(ws_url);
        } else {
          console.log("您的浏览器不支持websocket");
        }
        this.socket.onopen = this.websocketonopen;
        this.socket.onerror = this.websocketonerror;
        this.socket.onmessage = this.websocketonmessage;
        this.socket.onclose = this.websocketclose;
      } catch (e) {
        this.reconnect();
      }
    },
    websocketonopen() {
      //连接建立之后执行send方法发送数据
      console.log("WebSocket连接成功", this.socket.readyState);
      this.websocketsend();
    },
    websocketonerror(e) {
      //连接建立失败重连
      console.log("WebSocket连接发生错误", e);
      this.reconnect();
    },
    websocketonmessage(e) {
      //数据接收
      const data = JSON.parse(e.data);
      this.results.push(data["text"]);
      // console.log("得到响应", data);
      // 消息获取成功，重置心跳
      this.scrollToBottom();
    },
    websocketclose(e) {
      //关闭连接
      console.log("ws连接已断开 (" + e.code + ")");
      // this.reconnect();
      this.getList();
    },
    websocketsend() {
      //数据发送
      this.socket.send(JSON.stringify(this.temp));
    },
  },
  destroyed() {
    this.socket.close(); //离开路由之后断开websocket连接
  },
};
</script>


<style lang="scss" scoped>
.infinite-list {
  max-height: 600px;
  padding: 0;
  margin: 0;
  list-style: none;
  overflow: scroll;
  -ms-overflow-style: none;
  overflow: -moz-scrollbars-none;
  &::-webkit-scrollbar {
    width: 0px;
  }
  .infinite-list-item {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 38px;
    background: #ccdcec;
    margin: 10px;
    color: #429bf3;
    border-radius: 10px;
  }
}
.text {
  background: #000;
  height: 600px;
  border: 1px solid #e6e6e6;
  border-radius: 10px;
  padding: 10px 20px;
  overflow: scroll;
  -ms-overflow-style: none;
  overflow: -moz-scrollbars-none;
  &::-webkit-scrollbar {
    width: 0px;
  }
  .emoji {
    position: relative;
    width: 80%;
    height: 40px;
    line-height: 40px;
    font-size: 18px;
    padding: 0 20px;
    color: #07e250;
    span {
      position: absolute;
      left: 0;
      margin-left: 5px;
    }
    input {
      position: absolute;
      left: 0;
      top: 6px;
      background-color: transparent;
      color: #fff;
      left: 170px;
      padding: 2px 10px;
      width: 100%;
      border: none;
      outline: none;
      resize: none;
    }
  }
  p {
    color: #07e250;
    padding: 2px 10px;
    width: 100%;
    border: none;
    outline: none;
    resize: none;
  }
}
</style>