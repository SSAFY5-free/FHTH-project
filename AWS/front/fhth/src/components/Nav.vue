<template>
  <el-menu
    id="Nav"
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
  >
    <el-menu-item id="img" style="margin-left: 50px">
      <h1>FHTH</h1>
    </el-menu-item>
    <el-menu-item index="1">Hello, {{ email }}</el-menu-item>

    <!-- <el-submenu index="2">
        <template slot="title">Workspace</template>
        <el-menu-item index="2-1">item one</el-menu-item>
        <el-menu-item index="2-2">item two</el-menu-item>
        <el-menu-item index="2-3">item three</el-menu-item>
        <el-submenu index="2-4">
          <template slot="title">item four</template>
          <el-menu-item index="2-4-1">item one</el-menu-item>
          <el-menu-item index="2-4-2">item two</el-menu-item>
          <el-menu-item index="2-4-3">item three</el-menu-item>
        </el-submenu>
      </el-submenu> -->
    <!-- <el-menu-item index="3" disabled>Info</el-menu-item> -->
    <el-button
      type="primary"
      size="default"
      style="margin: 5px 15px 5px auto"
      @click="logout"
    >
      Logout</el-button
    >
    <!-- <el-menu-item index="2" key=""> </el-menu-item> -->
  </el-menu>
</template>

<script>
import VueCookies from "vue-cookies";
import { mapState } from "vuex";
export default {
  computed: {
    ...mapState("userInfo", ["name", "host", "accessToken", "email"]),
  },
  data() {
    return {
      activeIndex: "1",
      activeIndex2: "1",
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    logout() {
      VueCookies.set("accessToken", null);
      window.location.href = "/login";
    },
  },
};
</script>

<style>
</style>