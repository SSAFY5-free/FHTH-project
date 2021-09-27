const express = require("express");
const router = express.Router();
const unauthService = require("../service/unauth");


router.post("/getAccessToken", async (req, res) => {
  unauthService
    .post_accessToken(req.body)
    .then((data) => {
      console.log(data);
      return res.json(data);
    })
    .catch((error) => {
      return res.status(500).json(error);
    });
});
router.post("/addAccount", async (req, res) => {
  unauthService
    .post_account(req.body)
    .then((data) => {
      return res.status(200).json(data);
    })
    .catch((error) => {
      return res.status(500).json(error);
    });
});
router.post("/setModule", async (req, res) => {
  unauthService
    .post_module(req.body)
    .then(() => {
      return res.send("ok");
    })
    .catch((error) => {
      return res.status(500).send(error);
    });
});

router.post("/verifyRobot", async (req, res) => {
  unauthService
    .post_verifyRobot(req.body)
    .then((data) => {
      return res.send("ok");
    })
    .catch((error) => {
      return res.status(500).send(error);
    });
});
router.post("/action", async (req, res) => {
  unauthService
    .post_action(req)
    .then((data) => {
      return res.send("ok");
    })
    .catch((error) => {
      return res.status(500).send(error);
    });
});
module.exports = router;
