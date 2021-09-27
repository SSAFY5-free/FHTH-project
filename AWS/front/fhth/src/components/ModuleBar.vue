<template>
  <div id="ModuleBar">
    <!-- {{cur}} -->
    <el-button
      style="height: 100px; width: 100px; margin: 0px"
      type="primary"
      size="default"
      v-for="(module, idx) in robots[cur.robot_idx].modules"
      :key="module.id"
      @click="onClick(idx)"
    >
      {{ module.name }}
    </el-button>
  </div>
</template>

<script>
import { mapMutations, mapState } from "vuex";

export default {
  components: {},
  computed: {
    ...mapState("mainInfo", ["robots", "cur"]),
  },
  methods: {
    ...mapMutations("mainInfo", ["SET_CUR_MODULE_IDX"]),
    onClick(idx) {
      this.$store.commit("mainInfo/SET_CUR_MODULE_IDX", idx);
    },
  },
  data() {
    return {
      connect_count: [0],
    };
  },
  mounted() {},
};
</script>

<style>
</style>