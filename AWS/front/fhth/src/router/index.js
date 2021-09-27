import Vue from "vue";
import VueRouter from "vue-router";
import VueCookies from "vue-cookies";

//
import Login from "../components/Login.vue";
import SignUp from "../components/SignUp";
//
import Main from "../views/auth/Main.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/signup",
    name: "signup",
    component: SignUp,
  },
  {
    path: "/main",
    name: "main",
    component: Main,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

//네비게이션 가드((뷰 라우터로 URL 접근에 대해서 처리할 수 있음)
router.beforeEach(async (to, from, next) => {
  //여기서 모든 라우팅이 대기 상태가 됨
  /**
   * to: 이동할 url 정보가 담긴 라우터 객체
   * from: 현재 url 정보가 담긴 라우터 객체
   * next: to에서 지정한 url로 이동하기 위해 꼭 호출해야 하는 함수
   * next() 가 호출되기 전까지 화면 전환되지 않음
   */

  if (VueCookies.get("accessToken")) {
    console.log("router : pair success");
    return next();
  }
  if (VueCookies.get("accessToken") === null) {
    //토큰이 모두 없을 경우 로그인페이지로
    if (to.path === "/login" || to.path === "/signup") return next();
    else {
      alert("세션 권한이 없습니다.");
      return next({ path: "/login" });
    }
  }
});

export default router;
