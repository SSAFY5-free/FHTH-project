<template>
  <div id="addDevice">
    <el-input
      id="robot.id"
      placeholder="시리얼 코드"
      v-model="form.serial"
      class="input-with-select"
      @change="validationCheck"
    >
    </el-input>
  </div>
</template>

<script>
import { robotAPI } from "../utils/axios";
export default {
  props: ["form_id"],
  data() {
    return {
      form: {
        serial: "",
      },
    };
  },
  methods: {
    async validationCheck() {
      const { result } = (await robotAPI.verifyRobot(this.form)).data;
      this.$emit("update", { id: this.form_id, validation: result });
    },
  },
};
</script>

<style>
.el-select .el-input {
  width: 110px;
}
</style>