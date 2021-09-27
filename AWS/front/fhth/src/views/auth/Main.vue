<template>
  <div id="Main" class="bc" style="height: 100%">
    <Nav></Nav>
    <div id="sideBar">
      <robot></robot>
      <module-bar></module-bar>
    </div>
    <div id="mainView">
      <module-view :modules="modules" :module="module"></module-view>
    </div>
  </div>
</template>
<script>
import Robot from "../../components/Robot.vue";
import ModuleView from "../../components/ModuleView.vue";
import { mapState } from "vuex";
import ModuleBar from "../../components/ModuleBar.vue";
import Nav from "../../components/Nav.vue";
// import User from "../../components/User.vue";
import io from "socket.io-client";
import { baseURL, port } from "../../utils/conf";

export default {
  components: {
    Robot,
    ModuleView,
    ModuleBar,
    Nav,
  },
  computed: {
    ...mapState("mainInfo", ["robots", "cur", "lst"]),

    modules() {
      return this.$store.state.mainInfo.robots[
        this.$store.state.mainInfo.cur.robot_idx
      ].modules;
    },
    module() {
      return this.$store.state.mainInfo.robots[
        this.$store.state.mainInfo.cur.robot_idx
      ].modules[this.$store.state.mainInfo.cur.module_idx];
    },
  },
  created() {
    this.$store.dispatch("userInfo/SET_SOCKET", {
      socket: io(baseURL + port.server, {
        withCredentials: true,
        extraHeaders: {
          "my-custom-header": "abcd",
        },
      }),
    });
    setInterval(() => {
      this.$store.dispatch("userInfo/EMIT_SOCKET", {
        namespace: "module",
        data: {
          id: this.modules[this.cur.module_idx].id,
        },
      });
    }, 2000);
  },
  async mounted() {
    this.$store.dispatch("mainInfo/GET_ROBOTS_FROM_SERVER");
    this.$store.dispatch("userInfo/GET_USER");
  },
};
</script>