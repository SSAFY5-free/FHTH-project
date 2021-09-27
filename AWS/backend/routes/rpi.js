const express = require("express");
const router = express.Router();
require("../utils/session")(router);
const service = require("../service/rpi");
router.post("/session", (req, res) => {
  service
    .post_session(req)
    .then((data) => {
      res.send(data);
    })
    .catch((error) => {
      res.status(500).send("error");
    });
});
// router.get("/session", (req, res) => {
//   service.get_session()
//   .then((data)=> {

//   }).catch((data) => {

//   })
// });
module.exports = router;
