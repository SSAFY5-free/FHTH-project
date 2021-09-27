<template>
  <div class="block">
    <!-- <span class="demonstration">With default time</span> -->
    <el-date-picker
      v-model="timeReservation"
      type="datetime"
      placeholder="Select date and time"
      default-time="12:00:00"
    >
    </el-date-picker>
    <async-btn
      v-for="command in lstCommand"
      :key="command.keyword"
      :keyword="command.keyword"
      :command="command.command"
      :payload="timeReservation"
    >
    </async-btn>
  </div>
</template>

<script>
import AsyncBtn from "../ModuleView/AsyncBtn.vue";
// import AsyncBtn from "../ModuleView/AsyncBtn.vue";
import AsyncBtnVue from "../ModuleView/AsyncBtn.vue";
export default {
  components: { AsyncBtn },
  // components: { AsyncBtn },
  component: {
    AsyncBtnVue,
  },
  data() {
    return {
      lstCommand: [
        {
          keyword: "밥주기",
          command: "feed",
        },
      ],
      pickerOptions: {
        shortcuts: [
          {
            text: "Today",
            onClick(picker) {
              picker.$emit("pick", new Date());
            },
          },
          {
            text: "Yesterday",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit("pick", date);
            },
          },
          {
            text: "A week ago",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", date);
            },
          },
        ],
      },
      value1: "",
      value2: "",
      timeReservation: "",
    };
  },
};
</script>

<style>
</timeReservation>