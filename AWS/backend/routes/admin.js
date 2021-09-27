const express = require("express");
const db = require("../models").default
const router = express.Router();
require("../models");

router.post("/addRobot", async (req, res) => {
  const { serial, modules_id, name } = req.body;
  const result = await db["robots"].create({ serial, modules_id, name });
  // console.log(result);

  if (!result) res.json({ result: 0 });
  else res.json({ result: 1 });
  return;
});

router.post("/addAccount", async (req, res) => {
  const { email, pw, robots_id } = req.body;
  console.log(email, pw, robots_id);
  db["users"].create(
    {
      email,
      pw,
      robots_id,
    },
    function (err) {
      console.log(err);
    }
  );
  console.log("계정생성");
  return res.send({ result: 1 });
});

router.get("/addModuleType/:name", async (req, res) => {
  db["moduleTypes"].create({ ...req.params })
    .then((data) => {
      console.log(data);
      return res.send("ok");
    })
    .catch((err) => {
      return res.status("200").send("err");
    });
});
router.post("/addRegistedModule/", async (req, res) => {
  const { serial, type_id, data, name } = req.body;
  db["registedModules"].create({ serial, type_id, data, name })
    .then((data) => {
      console.log(data);
    })
    .then((data) => {
      console.log(data);
    });
  return res.json({ result: 1 });
});
module.exports = router;
