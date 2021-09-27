const express = require("express");
const jwt = require("jsonwebtoken");

const router = express.Router();
const path = require("path");
const authService = require("../service/auth");

require("dotenv").config({
  path: path.resolve(process.cwd(), ".env"),
});

const Verify = async (req, res, next) => {
  const accessToken = req.headers["x-access-token"];
  if (!accessToken) {
    return res.json({ error: "로그인 토큰을 가지고 있지 않습니다" });
  }
  next();
};
router.use(Verify);

router.post("/getRobots", async (req, res) => {
  await authService
    .get_robots(req)
    .then((data) => {
      res.send(data);
    })
    .catch((error) => {
      console.log(error);
      res.json("error");
    });
});

router.get("/getUser", async (req, res) => {
  await authService
    .get_user(req)
    .then((data) => {
      return res.json(data);
    })
    .catch((error) => {
      console.log(error);
      return res.json("error");
    });
});
router.post("/getModule", async (req, res) => {
  await authService
    .get_module(req)
    .then((data) => {
      return res.json(data);
    })
    .catch((error) => {
      console.log(error);
      return res.json("error");
    });
});

router.post("/moduleCmd", async (req, res) => {
  console.log(req.body);
  await authService.post_moduleCmd(req)
    .then((data) => {
      console.log("[Success] routes /moduleCmd ", data)
      return res.status(200).json(data)
    }).catch((error) => {
      // console.log("response : ", error.message)
      return res.status(500).json({ message: error.message });
    })
});

router.post("/getModules", async (req, res) => {
  await authService
    .get_modules(req)
    .then((data) => {
      return res.json(data);
    })
    .catch((error) => {
      console.log(error);
      return res.json("error");
    });
});

module.exports = router;
