<template>
  <div id="ModuleBtn">
    <module-btn
      style="height: 100px; width: 100px; margin: 0px"
      type="primary"
      size="default"
      v-for="(module, idx) in robots[cur.robot_idx].modules"
      :key="module.id"
      :loading="!module.clickable"
      @click="onClick(idx)"
    >
    </module-btn>
  </div>
</template>

<script>
export default {};
</script>

<style>
</style>