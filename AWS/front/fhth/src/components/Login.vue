<template>
  <el-card id="Login" style="width: 400px; margin: auto">
    <img alt="Vue logo" src="../assets/logo(1).png" />
    <el-form :label-position="labelPosition" label-width="100px" :model="form">
      <el-form-item label="email">
        <el-input v-model="form.email"></el-input>
      </el-form-item>
      <el-form-item label="pw">
        <el-input v-model="form.pw"></el-input>
      </el-form-item>
    </el-form>
    <span>
      <el-button @click="login" type="primary">Login</el-button>
    </span>
  </el-card>
</template>

<script>
import { userAPI } from "../utils/axios";

export default {
  data() {
    return {
      labelPosition: "left",
      form: {
        email: "",
        pw: "",
      },
    };
  },
  methods: {
    async login() {
      const { email, pw } = this.form;
      if (!email || !pw) {
        return alert("이메일과 비밀번호를 입력해주세요");
      }
      //서버에 로그인 요청
      await userAPI.login(email, pw).then((res) => {
        const { data } = res;
        if (data.accessToken) {
          // 토큰을 쿠키에 저장
          console.log(data);
          this.$store.commit("userInfo/loginToken", data);
          this.$router.push("/main");
        } else {
          // 로그인 실패
          alert("이메일과 비밀번호를 다시 입력해주세요");
          this.form.pw = "";
        }
      });

      //로그인 성공시
    },
  },
};
</script>

<style>
.Login {
  display: inline-block;
  margin: 0 10px;
}
/* .home {
  border: 1px solid black;
  display: flex;
  flex-direction: column;
  align-items: center;
} */
</style>
