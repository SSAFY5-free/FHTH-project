const jwt = require("jsonwebtoken");

// const { db["User"], RegistedModule, Robot, Session } = require("../models");
const db = require("../models").default;

exports.post_accessToken = (data) => {

  return new Promise(async (resolve, reject) => {

    try {
      const { email, pw, name } = data;
      const result = await db["users"].findOne({ email, pw });
      //검색 결과가 없으면
      // console.log(result);
      if (!result) resolve();
      else {
        //accessToken 발급
        const accessToken = jwt.sign(
          {
            email: result.email,
            user_id: result.id
          },
          "fhth",
          {
            expiresIn: "1h",
          }
        );
        // console.log(result);
        return resolve({
          accessToken, email: "Zz"
        });
      }
    } catch (error) {
      console.log(error);
      return reject();
    }
  });
};

exports.post_account = (data) => {
  return new Promise(async (resolve, reject) => {
    try {
      const { email, pw, robot } = data;
      db["users"].create(
        {
          email,
          pw,
          robot,
        },
        function (err) {
          console.log(err);
        }
      );
      return resolve();
    } catch (error) {
      console.log(error);
      return reject();
    }
  });
};

exports.post_module = (payload) => {
  return new Promise(async (resolve, reject) => {
    try {
      const { module_id, data } = payload;
      console.log(module_id, data);

      await db["registedModules"].findOneAndUpdate({
        id: module_id
      }, { data });
      return resolve();
    } catch (error) {
      console.log(error);
      return reject();
    }
  });
};

exports.post_verifyRobot = (data) => {
  return new Promise(async (resolve, reject) => {
    try {
      const { serial } = data;
      const result = await db["robots"].findOne({ serial });
      return resolve(result);
    } catch (error) {
      console.log(error);
      return reject();
    }
  });
};

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

exports.post_action = (req) => {
  return new Promise(async (resolve, reject) => {
    try {
      // 로직 1. module_id와 contents, timestamp 추출
      const { module_id, content, timestamp } = req.body
      addAction(module_id, content, timestamp)
      // 로직 2. registedModules에 저장
      return resolve()
    }
    catch {
      return reject()
    }
  })
}