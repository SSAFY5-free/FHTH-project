import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);
import userInfo from "@/store/userInfo.js";
import mainInfo from "@/store/mainInfo.js";
// import createPersistedState from "vuex-persistedstate";

export default new Vuex.Store({
  // plugins: [createPersistedState({})],
  state: {},
  mutations: {},
  actions: {},
  getters: {},
  modules: {
    userInfo,
    mainInfo,
  },
});
