<template>
  <el-button
    type="primary"
    size="default"
    :loading="isLoading"
    @click="onClick"
  >
    {{ keyword }}
  </el-button>
</template>

<script>
import { moduleAPI } from "../../utils/axios";
import { mapState } from "vuex";
export default {
  props: ["keyword", "command", "payload"],
  computed: {
    ...mapState("mainInfo", ["robots", "cur"]),
  },
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    async onClick() {
      //로직 1. robot_id, module_id = 명령을 내릴 로봇과 module의 id
      const robot = this.robots[this.cur.robot_idx];
      const robot_id = robot.id;
      const module_id = robot.modules_id[this.cur.module_idx];

      //로직 2. command, payload = 명령 내릴 종류와 명령 내용
      const command = this.command;
      const payload = this.payload;

      // console.log("AsyncBtn : ", robot_id, module_id);

      this.isLoading = true;
      await moduleAPI
        .command({ robot_id, module_id, command, payload })
        .then((res) => {
          const { data } = res;
          if (data.status == -1) {
            alert(data.message);
          } else {
            //todo 모듈 동작상태 저장하는 axios 생성
          }
        })
        .catch((error) => {
          error;
          console.log(error);
          // console.log("에러 : ", error);
        });
      this.isLoading = false;
      window.location.href = "/FHTH_free/main";
    },
  },
};
</script>

<style>
</style>