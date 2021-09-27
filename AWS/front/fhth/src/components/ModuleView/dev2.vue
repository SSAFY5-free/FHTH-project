<template>
  <div id="dev2">
    <!-- <div slot="header" class="clearfix"> -->
    <!-- <span>dev1 : {{ module.name }}</span> -->
    <!-- </div> -->

    <!-- 모듈 이미지 -->
    <!-- <div id="describe">img</div> -->

    <!-- 모듈 이름 -->
    <!-- <p>status of {{ module.name }}</p> -->
    <el-card class="box-card" id="info">
      <div slot="header" class="clearfix header">
        <el-tooltip
          effect="light"
          content="급식기의 정보를 나타냅니다"
          placement="top-start"
        >
          <b>Info</b>
        </el-tooltip>
      </div>

      <div>
        <div>
          <el-tooltip
            effect="light"
            content="급수기를 이용한 시간을 나타냅니다"
            placement="top"
          >
            <!-- <span class="demonstration">last time</span> -->
            <el-date-picker
              v-model="data.timeWater"
              type="datetime"
              placeholder="예약할 시간"
            >
            </el-date-picker>
          </el-tooltip>
        </div>
        <div style="flex: 1">
          <el-tooltip
            effect="light"
            content="급수기에 남은 물 양을 true/false 나타냅니다."
            placement="top"
          >
            <el-progress
              :percentage="data.isWater ? 100 : 0"
              :color="colors"
              type="circle"
            ></el-progress>
          </el-tooltip>
        </div>
      </div>
    </el-card>
    <el-card class="box-card" id="control">
      <div slot="header" class="clearfix header">
        <el-tooltip effect="light" placement="top-start">
          <div slot="content">급식기의 명령 인터페이스입니다.</div>
          <b>Control</b>
        </el-tooltip>
      </div>
      <div style="display: flex; justify-content: center">
        <el-tooltip
          effect="light"
          content="동작할 시간을 설정합니다."
          placement="left-start"
        >
          <!--todo 예약 목록 인터페이스 추가 -->
          <h1 style="color: #e5e4e2">Blank</h1>
        </el-tooltip>
      </div>
    </el-card>
  </div>
</template>

<script>
import AsyncBtn from "./AsyncBtn.vue";
import DateTimePicker from "../element-ui/dateTimePicker.vue";
import moment from "moment";
export default {
  components: {},
  componets: {
    AsyncBtn,
    DateTimePicker,
  },
  props: ["module"],
  data() {
    return {
      //progress circle 색 종류
      colors: [
        { color: "#f56c6c", percentage: 20 },
        { color: "#e6a23c", percentage: 40 },
        { color: "#5cb87a", percentage: 60 },
        { color: "#1989fa", percentage: 80 },
        { color: "#6f7ad3", percentage: 100 },
      ],

      //버튼 종류
      lstCommand: [
        {
          keyword: "예약",
          command: "reserve",
        },
        {
          keyword: "밥주기",
          command: "feed",
        },
      ],
      data: this.module.data,
    };
  },
  methods: {
    onClick() {},
    seteatTime(date) {
      this.eatTime = moment(date).toDate();
    },
  },
};
</script>

<style>
</style>