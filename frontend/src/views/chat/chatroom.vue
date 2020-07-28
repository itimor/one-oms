<template>
  <div class="chat-app">
    <div class="chat-container">
      <div class="chat-sider">
        <mycard></mycard>
      </div>

      <div class="chat-main">
        <div class="chat-group">
          <div class="chat-search">
            <el-input
              type="text"
              class="searchInput"
              v-model="listQuery.search"
              suffix-icon="el-icon-search"
              placeholder="搜索"
            />
          </div>
          <div class="chat-group-list">
            <ul>
              <li
                v-for="item in group_list"
                :key="item.id"
                class="group-list"
                :class="{ active: item.id === selectId }"
                @click="selectGroup(item)"
              >
                <div class="list-left">
                  <img
                    class="avatar"
                    width="42"
                    height="42"
                    :alt="item.name"
                    :src="item.create_user.avatar"
                  />
                </div>
                <div class="list-right">
                  <span class="time">{{item.messages[item.messages.length-1].create_time|chatTime}}</span>
                  <p class="name">{{item.name}}</p>
                  <p class="lastmsg">{{item.messages[item.messages.length-1].message}}</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
        <div v-if="selectId<1" class="chat-message">
          <p class="empty_tip">点击左侧群组，开启奇妙对话</p>
        </div>
        <div v-else class="chat-message">
          <div class="message">
            <header class="header">
              <div class="friendname">
                {{selectName}}
                <span>
                  <i class="el-icon-more"></i>
                </span>
              </div>
            </header>
            <div class="message-wrapper" ref="list_message">
              <ul>
                <li v-for="item in message_list" :key="item.id" class="message-item">
                  <div class="time">
                    <span>{{item.create_time | chatTime}}</span>
                  </div>
                  <div class="main" :class="item.create_user.id===user_id?'self':'other'">
                    <img class="avatar" width="36" height="36" :src="item.create_user.avatar" />
                    <div class="content">
                      <div class="message-text" v-html="item.message"></div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
          <div class="text">
            <div class="emoji">
              <i class="icon icon-lock el-icon-picture-outline-round"></i>
              <i class="icon icon-look el-icon-folder"></i>
              <i class="icon icon-look el-icon-scissors"></i>
              <i class="icon icon-look el-icon-chat-dot-round"></i>
            </div>
            <textarea ref="text" v-model="temp.message" @keyup="onKeyup"></textarea>
            <div class="send" @click="sendMessage">
              <span>发送(S)</span>
            </div>
            <transition name="appear">
              <div class="warn" v-show="empty_warn">
                <div class="description">不能发送空白信息</div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { chatgroup, chatmessage } from "@/api/all";
import { mapGetters } from "vuex";
import mycard from "./pages/mycard";

const heartCheck = {
  timeout: 60 * 1000,
  timer: null,
  serverTimer: null,
  reset() {
    this.timer && clearTimeout(this.timer);
    this.serverTimer && clearTimeout(this.serverTimer);
  },
  start(ws) {
    this.reset();
    this.timer = setTimeout(() => {
      console.log("发送心跳,后端收到后，返回一个心跳消息");
      // onmessage拿到返回的心跳就说明连接正常
      ws.send(JSON.stringify({ heart: 1 }));
      this.serverTimer = setTimeout(() => {
        // 如果超过一定时间还没响应(响应后触发重置)，说明后端断开了
        ws.close();
      }, this.timeout);
    }, this.timeout);
  },
};

export default {
  name: "chatroom",

  components: { mycard },
  data() {
    return {
      group_list: [],
      message_list: [],
      selectId: "",
      selectName: "",
      empty_warn: false,
      listQuery: {
        search: "",
        join_user: "",
        group: undefined,
      },
      temp: {
        create_user: "",
        group: "",
        message: "",
      },
      room_name: "",
      ws_uri: "/ws/chat/", // ws path
      lockReconnect: false, // 连接失败不进行重连
      maxReconnect: 5, // 最大重连次数，若连接失败
      socket: null,
    };
  },
  computed: {
    ...mapGetters(["user_id"]),
  },
  created() {
    this.getGroupList();
  },
  mounted() {
    //   this.initWebSocket();
  },
  destroyed() {
    this.socket.close(); //离开路由之后断开websocket连接
  },
  methods: {
    getGroupList() {
      this.listQuery.join_user = this.user_id;
      chatgroup.requestGet(this.listQuery).then((response) => {
        this.group_list = response.results;
        for (var i of this.group_list) {
          this.initWebSocket(i.code);
        }
      });
    },
    getMessageList(group_id) {
      const data = {
        group: group_id,
      };
      chatmessage.requestGet(data).then((response) => {
        this.message_list = response.results;
      });
    },
    scrollToBottom() {
      //  在页面加载时让信息滚动到最下面
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs.list_message.scrollTop = this.$refs.list_message.scrollHeight;
        }, 0);
      });
    },
    selectGroup(row) {
      this.message_list = [];
      this.room_name = row.code;
      this.selectId = row.id;
      this.selectName = row.name;
      this.message_list = row.messages;
      this.scrollToBottom();
      //this.getMessageList(row.id);
      this.temp = {
        user_id: this.user_id,
        group_id: row.id,
        message: "",
      };
    },
    // 按回车发送信息
    onKeyup(e) {
      if (e.keyCode === 13) {
        this.sendMessage();
      }
    },
    sendMessage() {
      // 当输入框中的值为空时 弹出提示  并在一秒后消失
      if (this.temp.message.replace(/[\r\n]/g, "") === "") {
        this.empty_warn = true;
        setTimeout(() => {
          this.empty_warn = false;
        }, 1000);
      } else {
        this.websocketsend();
      }
      this.temp.message = "";
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
        console.log(123);
        this.reconnect();
      }
    },
    websocketonopen() {
      //连接建立之后执行send方法发送数据
      console.log("WebSocket连接成功", this.socket.readyState);
      heartCheck.start(this.socket);
    },
    websocketonerror(e) {
      //连接建立失败重连
      console.log("WebSocket连接发生错误", e);
      this.reconnect();
    },
    websocketonmessage(e) {
      //数据接收
      const data = JSON.parse(e.data);
      this.message_list.push(data);
      // console.log("得到响应", data);
      // 消息获取成功，重置心跳
      this.scrollToBottom();
      heartCheck.start(this.socket);
    },
    websocketclose(e) {
      //关闭连接
      console.log("ws连接已断开 (" + e.code + ")");
      this.reconnect();
    },
    websocketsend() {
      //数据发送
      this.socket.send(JSON.stringify(this.temp));
    },
  },
};
</script>


<style lang="scss" scoped>
ul {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font-weight: normal;
  vertical-align: baseline;
  li {
    list-style: none;
  }
}
.chat-app {
  height: 600px;
  .chat-container {
    font-family: "Microsoft YaHei";
    flex: 1;
    border-radius: 10px;
    margin: 20px auto;
    width: 860px;
    height: 600px;
    background-color: #ffffff;
    .chat-sider {
      width: 60px;
      height: 600px;
      background: #2b2c2f;
      float: left;
    }
    .chat-main {
      display: flex;
      width: 800px;
      height: 600px;
      background: #f2f2f2;
      .chat-group {
        width: 250px;
        background: rgb(230, 230, 230);
        .chat-search {
          padding: 22px 12px 12px 12px;
        }
        .chat-group-list {
          height: 540px;
          overflow-y: auto;
          .group-list {
            display: flex;
            padding: 12px;
            transition: background-color 0.1s;
            font-size: 0;
            &:hover {
              background-color: rgb(220, 220, 220);
            }
            &.active {
              background-color: #c4c4c4;
            }
            .avatar {
              border-radius: 2px;
              margin-right: 12px;
            }
            .list-right {
              position: relative;
              flex: 1;
              margin-top: 4px;
              height: 25px;
              line-height: 0;
              .time {
                float: right;
                color: #999;
                font-size: 10px;
                vertical-align: bottom;
              }
              .name {
                position: absolute;
                font-size: 14px;
                width: 130px;
                height: 15px;
                line-height: 15px;
                bottom: 1px;
                overflow: hidden;
                white-space: nowrap;
                text-overflow: ellipsis;
              }
              .lastmsg {
                font-size: 12px;
                color: #999;
                display: inline-block;
                line-height: 30px;
              }
            }
          }
        }
      }
      .chat-message {
        width: 550px;
        flex: 1;
        .empty_tip {
          color: #999;
          font-size: 26px;
          line-height: 500px;
          vertical-align: middle;
          text-align: center;
        }
        .message {
          width: 100%;
          height: 450px;
          .header {
            height: 60px;
            padding: 28px 0 0 30px;
            box-sizing: border-box;
            border-bottom: 1px solid #e7e7e7;
            .friendname {
              font-size: 18px;
              span {
                float: right;
                color: #999;
                margin: 0 20px;
                i {
                  &:hover {
                    color: #2b2c2f;
                  }
                }
              }
            }
          }
          .message-wrapper {
            min-height: 390px;
            max-height: 390px;
            padding: 10px 15px;
            box-sizing: border-box;
            overflow-y: auto;
            border-bottom: 1px solid #e7e7e7;
            .message {
              margin-bottom: 15px;
            }
            .time {
              width: 100%;
              font-size: 12px;
              margin: 7px auto;
              text-align: center;
              span {
                display: inline-block;
                padding: 4px 6px;
                color: #fff;
                border-radius: 3px;
                background-color: #dcdcdc;
              }
            }
            .main {
              .avatar {
                float: left;
                margin-left: 15px;
                border-radius: 3px;
              }
              .content {
                display: inline-block;
                margin-left: 10px;
                position: relative;
                padding: 6px 10px;
                max-width: 330px;
                min-height: 36px;
                line-height: 24px;
                box-sizing: border-box;
                font-size: 14px;
                text-align: left;
                word-break: break-all;
                background-color: #fafafa;
                border-radius: 4px;
                &:before {
                  content: " ";
                  position: absolute;
                  top: 12px;
                  right: 100%;
                  border: 6px solid transparent;
                  border-right-color: #fafafa;
                }
              }
            }
            .self {
              text-align: right;
              .avatar {
                float: right;
                margin: 0 15px;
              }
              .content {
                background-color: #b2e281;
                &:before {
                  right: -12px;
                  vertical-align: middle;
                  border-right-color: transparent;
                  border-left-color: #b2e281;
                }
              }
            }
          }
        }
      }
      .text {
        position: relative;
        height: 150px;
        background: #fff;
        border-right: 1px solid #e6e6e6;
        .emoji {
          position: relative;
          width: 100%;
          height: 40px;
          line-height: 40px;
          font-size: 18px;
          padding: 0 20px;
          box-sizing: border-box;
          color: #7c7c7c;
          .icon-look {
            padding: 0 5px;
            cursor: pointer;
            &:hover {
              color: #90ec90;
            }
          }
        }
        textarea {
          box-sizing: border-box;
          padding: 5px 20px;
          height: 110px;
          width: 100%;
          border: none;
          outline: none;
          resize: none;
          border-bottom: 1px solid #e6e6e6;
        }
        .send {
          position: absolute;
          bottom: 10px;
          right: 10px;
          width: 75px;
          height: 28px;
          line-height: 28px;
          box-sizing: border-box;
          text-align: center;
          border: 1px solid #e5e5e5;
          border-radius: 3px;
          background: #f5f5f5;
          font-size: 14px;
          color: #7c7c7c;
          &:hover {
            background: rgb(18, 150, 17);
            color: #fff;
          }
        }
        .warn {
          position: absolute;
          bottom: 50px;
          right: 10px;
          width: 110px;
          height: 30px;
          line-height: 30px;
          font-size: 12px;
          text-align: center;
          border: 1px solid #bdbdbd;
          border-radius: 4px;
          box-shadow: 0 1px 5px 1px #bdbdbd;
          &.appear-enter-active,
          &.appear-leave-active {
            transition: all 1s;
          }
          &.appear-enter,
          &.appear-leave-active {
            opacity: 0;
          }
          &:before {
            content: " ";
            position: absolute;
            top: 100%;
            right: 20px;
            border: 7px solid transparent;
            border-top-color: #fff;
            filter: drop-shadow(1px 3px 2px #bdbdbd);
          }
        }
      }
    }
  }
}
</style>