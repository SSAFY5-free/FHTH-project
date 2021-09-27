import axios from "axios";
import VueCookies from "vue-cookies";
import conf from "../utils/conf";

const request = axios.create({
  baseURL: conf.baseURL + conf.port.server,
  timeout: 3000
});
request.interceptors.request.use(
  async function (config) {
    config.headers["x-access-token"] = VueCookies.get("accessToken");
    config.headers["Content-Type"] = "application/json";
    return config;
  },
  function (error) {
    console.log("axios request error : ", error);
    return Promise.reject(error);
  }
);

request.interceptors.response.use(
  function (response) {
    try {
      return response;
    } catch (err) {
      console.error("[axios.interceptors.response] response : ", err.message);
    }
  },
  async function (error) {
    return Promise.reject(error);
  }
);

export const userAPI = {
  login: (email, pw) => {
    const result = request.post("/unauth/getAccessToken", {
      email,
      pw,
      name,
    });
    console.log(result);
    return result;
  },
  signup: (form) => {
    return request.post("/unauth/addAccount", form);
  },
  getUser: () => {
    console.log("robot_API_GET_USER");
    return request.get("/auth/getUser");
  },
};

export const robotAPI = {
  getRobots: () => {
    return request.post("/auth/getRobots");
  },
  verifyRobot: (form) => {
    return request.post("/unauth/verifyRobot", { form });
  },
  getModules: (id) => {
    console.log("robotAPI _ GETMODULES : ");
    return request.post("/auth/getModules", { id });
  },
  getModule: (id) => {
    console.log("robotAPI _ GETMODULE : ");
    return request.post("/auth/getModule", { id });
  },
};

export const moduleAPI = {
  command: async (data) => {
    const res = await request
      .post("/auth/moduleCmd",
        data,
      ).then((data) => {
        return data
      })
      .catch((error) => {
        // alert(error);
        return error;
      });
    return res
  },
};
