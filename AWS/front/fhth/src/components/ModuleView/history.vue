<template>
  <div class="block">
    <!-- {{ actions }} -->
    <div class="radio">
      Order:
      <el-radio-group v-model="reverse">
        <el-radio :label="true">descending</el-radio>
        <el-radio :label="false">ascending</el-radio>
      </el-radio-group>
    </div>
    <!-- {{ actions }} -->
    <el-timeline :reverse="reverse">
      <el-timeline-item
        v-for="(activity, index) in actions"
        :key="index"
        :timestamp="activity.timestamp"
      >
        {{ activity.content }}
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script>
export default {
  props: ["actions"],
  data() {
    return {
      reverse: true,
    };
  },
};
</script>

<style>
</style>