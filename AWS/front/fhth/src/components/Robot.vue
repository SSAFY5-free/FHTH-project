<template>
  <el-card id="Robot" shadow="always" :body-style="{ padding: '20px' }">
    <div slot="header">
      <el-select v-model="value" placeholder="Select" @change="onChange(value)">
        <el-option
          v-for="(robot, idx) in lst.robots"
          :key="robot.name"
          :label="robot.name"
          :value="idx"
        >
        </el-option>
      </el-select>
    </div>

    <!-- card body -->

    <!-- <p>robot_id : {{ lst }}</p> -->
    <!-- <p>robots : {{ robots }}</p> -->
    <div style="display: flex"></div>
    <div id="screen" class="bc">
      <img src="http://172.30.1.7:8091/stream.mjpg" alt="" width="400px" height="300px" style="transform:rotate(180deg)"/>
    </div>
    <div id="keyPad">
      <div>
        <div></div>
        <div>
          <el-button
            type="primary"
            size="default"
            icon="el-icon-caret-top"
            @click="onClick('go')"
          ></el-button>
        </div>

        <div></div>
      </div>
      <div>
        <div>
          <el-button
            type="primary"
            size="default"
            icon="el-icon-caret-left"
            @click="onClick('left')"
          ></el-button>
        </div>
        <div>
          <el-button
            type="primary"
            size="default"
            icon="el-icon-circle-close"
            @click="onClick('stop')"
          ></el-button>
        </div>
        <div>
          <el-button
            type="primary"
            size="default"
            icon="el-icon-caret-right"
            @click="onClick('right')"
          ></el-button>
        </div>
      </div>
      <div>
        <div></div>
        <div>
          <el-button
            type="primary"
            size="default"
            icon="el-icon-caret-bottom"
            @click="onClick('back')"
          ></el-button>
        </div>
        <div>
          <el-button
            type="primary"
            size="default"
            @click="onClick('middle')"
            icon="el-icon-d-caret"
          ></el-button>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import { mapState } from "vuex";
export default {
  computed: {
    ...mapState("mainInfo", ["robots", "cur", "lst"]),
    curRobot_idx() {
      return this.cur.robot_idx;
    },
  },
  data() {
    return {
      value: "",
    };
  },
  methods: {
    onChange(idx) {
      this.cur.robot_idx = idx;
    },
    onClick(direction) {
      const robot_id = this.robots[this.cur.robot_idx].id;
      this.$store.dispatch("userInfo/EMIT_SOCKET", {
        namespace: "command",
        data: {
          robot_id,
          direction,
        },
      });
    },
    created() {
      this.onChange(0);
    },
  },
};
</script>
<style>
</style>