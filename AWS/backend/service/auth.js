const express = require("express");
const jwt = require("jsonwebtoken");
const db = require("../models").default;
const db_connected = require("../models")
const { robotAPI } = require("../utils/axios")

//.env파일에서 파라미터 호출. process.env.
const dotenv = require("dotenv")
dotenv.config({})

exports.get_robots = (req) => {
  return new Promise(async (resolve, reject) => {
    try {
      const accessToken = req.headers["x-access-token"];

      //로직 1. 토큰에서 user_id 추출
      const { email } = jwt.decode(accessToken, "fhth");
      console.log("user email : ", email)

      //로직 2. robot_id = 유저가 소유한 로봇의 아이디
      const { robots_id } = await db["users"].findOne({ email });

      //로직 3. robots = 유저의 로봇 데이터 조회
      const robots = await robots_id.reduce(async (promise, id) => {
        const acc = await promise.then();
        const robot = await db["robots"].findOne({ id });
        acc.push(robot);
        return Promise.resolve(acc);
      }, Promise.resolve([]));
      //console.log("user robots : ", robots)

      //로직 4. 로봇 정보를 반환
      if (robots) return resolve(robots);
      else return resolve("");

    } catch (error) {
      reject(error);
    }
  });
};
exports.get_user = (req) => {
  return new Promise(async (resolve, reject) => {
    try {
      //로직 1. user_id = 유저 id를 토큰에서 추출
      const accessToken = req.headers["x-access-token"];
      const user_id = jwt.decode(accessToken, "fhth").user_id;

      //로직 2. email, name = 조회한 유저 데이터
      console.log(user_id)
      const { email, name } = await db["users"].findOne({ id: user_id });
      return resolve({ email, name });

    } catch (error) {
      return reject(error);
    }
  });
};

exports.get_module = (req) => {
  return new Promise(async (resolve, reject) => {
    try {
      //로직 1. id = 조회하려는 모듈 id
      const { id } = req.body;

      //로직 2. result = 모듈의 데이터
      const result = await db["registedModules"].findOne({ id });
      return resolve(result);

    } catch (error) {
      return reject(error);
    }
  });
};
exports.get_modules = (req) => {
  return new Promise(async (resolve, reject) => {
    try {

      //로직 1. id = 조회하려는 로봇의 id
      const { id } = req.body;

      //로직 2. modules_id = 로봇에 연결된 모듈의 id
      const { modules_id } = await db["robots"].findOne({ id });

      //로직 3. result = 로봇에 연결된 모듈들의 데이터
      const result = await modules_id.reduce(async (promise, id) => {
        const acc = await promise.then();
        const data = await db["registedModules"].findOne({ id });
        acc.push(data);
        return acc;
      }, Promise.resolve([]));

      return resolve(result);
    } catch (error) {
      return reject(error);
    }
  });
};

exports.post_moduleCmd = (req) => {
  return new Promise(async (resolve, reject) => {
    try {
      //로직 1. 로봇의 ip 조회
      const { robot_id, module_id, command, payload } = req.body
      const { ip } = await db["robots"].findOne({ id: robot_id })



      //로직 3. 커맨드에 따라 TCP 통신 핸들링
      if (command == "feed") {

        await robotAPI.sendModuleCmd(ip, { command, payload })
          .then((data) => {
            //로직 2. 해당 모듈에 조작 이력 추가
            addAction(module_id, { timestamp: new Date(), content: command })
            console.log("[Success] post_moduleCmd", data)
            return resolve({ status: 1, message: "" })
          })
          .catch((error) => {
            const msg = `[Error] post_modCODEuleCmd" ${error}`
            return resolve({ status: -1, message: error.message })
          })
      }
      else if (command == "amount") {

        await robotAPI.sendModuleAmount(ip, { command, payload })
          .then((data) => {
            console.log("[Success] post_moduleCmd", data)
            return resolve(data)
          })
          .catch((error) => {
            const msg = `[Error] post_modCODEuleCmd" ${error}`
            return resolve(error)
          })
      }
    } catch (error) {
      return reject({ status: -1, msg: "post_moduleCmd" });
    }
  })
}

async function addAction(module_id, content, timestamp = new Date()) {
  /*
  module의 action 추가 로직
  */
  //todo 최적화
  const { actions } = await db["registedModules"].findOne({ id: module_id })
  actions.push({ content, timestamp })
  await db["registedModules"].update({ id: module_id }, {
    $set: {
      actions
    }
  })
}