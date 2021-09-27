<template>
  <div id="app">
    <div
      id="nav"
      v-if="$route.fullPath == '/login' || $route.fullPath == '/signup'"
    >
      <router-link to="/login">로그인</router-link> |
      <router-link to="/signup">회원가입</router-link>
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  components: {},
  methods: {},
  computed: {},
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-image: url("~@/assets/img/background.jpg");
  background-size: cover;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
