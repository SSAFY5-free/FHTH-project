<template>
  <el-card id="SignUp">
    <el-form
      :model="form"
      status-icon
      ref="ruleForm"
      label-width="80px"
      class="demo-ruleForm"
    >
      <el-form-item label="아이디">
        <el-input type="id" v-model="form.email" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="비밀번호">
        <el-input type="id" v-model="form.pw" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="비밀번호">
        <el-input type="id" v-model="form.pw" autocomplete="off"></el-input>
      </el-form-item>

      <div id="registedRobots">
        <!-- dynamic form -->
        <el-form-item
          v-for="robot in form.lstRobot"
          :key="robot.id"
          :label="String(robot.validation)"
          size="normal"
        >
          <add-Robot @update="validationCheck" :form_id="robot.id"></add-Robot>
        </el-form-item>
      </div>

      <el-form-item>
        <el-button @click="addDomain">새 디바이스</el-button>
        <el-button type="primary" @click="onSubmit">회원 가입</el-button>
        <!-- <el-button @click="resetForm('ruleForm')">Reset</el-button> -->
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import { userAPI } from "../utils/axios";
import addRobot from "./addRobot.vue";
export default {
  components: {
    addRobot,
  },
  data() {
    return {
      form: {
        email: "",
        pw: "",
        lstRobot: [
          {
            id: 0,
            type: "",
            serial: "",
            validation: 0,
          },
        ],
      },
      lstRobotCount: 0,
      deviceList: [],
    };
  },
  methods: {
    async onSubmit() {
      const result = await userAPI.signup(this.form);
      console.log(result);
    },
    addDomain() {
      this.form.lstRobot.push({
        id: ++this.lstRobotCount,
        type: "",
        serial: "",
        validation: 0,
      });
    },
    validationCheck(data) {
      console.log(data);
      this.form.lstRobot[data.id].validation = data.validation;
      // console.log("Zz", this.form.lstRobot[Number(data.id)].validation)
    },
  },
  async created() {},
};
</script>

<style>
</style>