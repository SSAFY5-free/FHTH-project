<template>
  <el-card id="ModuleView" class="box-card">
    <!-- <p>module : {{ module }}</p> -->
    <!-- <p>modules : {{ modules }}</p> -->
    <div slot="header">
      <b>{{ module.name }}</b>
    </div>
    <!-- {{ this.$store.state.mainInfo.cur.module_idx }} -->
    <div id="moduleStatus">
      <dev1 v-if="module.type_id == '1'" v-bind:module="module"></dev1>
      <dev2 v-if="module.type_id == '2'" v-bind:module="module"></dev2>
    </div>
    <div id="moduleHistory">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <el-tooltip
            effect="light"
            content="모듈 동작 이벤트를 보여줍니다."
            placement="top"
          >
            <b>History</b>
          </el-tooltip>
        </div>
        <history :actions="module.actions"></history>
      </el-card>
    </div>
  </el-card>
</template>
<script>
import dev1 from "./ModuleView/dev1.vue";
import dev2 from "./ModuleView/dev2.vue";
import history from "./ModuleView/history.vue";
import { mapState } from "vuex";
export default {
  components: {
    dev1,
    dev2,
    history,
  },
  computed: {
    ...mapState("mainInfo", ["robots", "cur"]),
  },
  props: ["modules", "module"],
  mounted() {
    console.log("mounted");
  },
};
</script>

<style>
</style>