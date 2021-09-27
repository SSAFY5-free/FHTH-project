var express = require("express");
// var DBus = require("dbus");
// var bus = DBus.getBus("session");
var router = express.Router();
const axios = require("axios");
var left = 0
var drink = false
var iseaten = false
var water = false
/* GET users listing. */
router.get("/", function (req, res, next) {
  res.send("HELLO JBJ");
});

//set_amount 제어
router.post("/feedcontrol", async function (req, res, next) {
  bus.getInterface("food.fhth","/fhth/food/Test", "food.fhth.TestInterface", function(err, iface) {
    if(err){
      console.log(err)
    }
    iface.set_amount(req.body.payload)
    console.log("success")
    res.send(req.body)
  })
});

//robot 제어
router.post("/control", async function (req, res, next) {
  bus.getInterface("motor.fhth","/fhth/motor/Test", "motor.fhth.TestInterface", function(err, iface) {
    if(err){
      console.log(err)
    }
    iface.activate_motor(req.body.payload)
    console.log("success")
    res.send(req.body)
  })
});


//밥주기 예약 및 밥 주기
router.post("/servefood", async function (req, res, next) {
  bus.getInterface("food.fhth","/fhth/food/Test", "food.fhth.TestInterface", function(err, iface) {
    if(err){
      console.log(err)
    }
    iface.activate_action()
    console.log("success")
    res.send("success")
  })
});

// 밥 먹은거 
router.post("/foodeat", async function (req, res, next) {
  iseaten = req.body.EATEN
  await axios
    .post("http://127.0.0.1:8079/unauth/setModule", {
      module_id: 2,
      data: {
        iseaten: iseaten,
        left: left,
        time: req.body.DATE
      },
    })
    .then((response) => {
      // console.log(req.body.data)
      res.send(req.body);
      // console.log(response.data);
      console.log(22222);
    })
    .catch(function (error) {
      res.send(error);
      console.log(11111);
      console.log(error);
    });
});
// 밥 남은거
router.post("/foodleft", async function (req, res, next) {
  left = req.body.LEFT
  res.json(req.body);
  await axios
    .post("http://127.0.0.1:8079/unauth/setModule", {
      module_id: 2,
      data: {
        iseaten: iseaten,
        left: left,
        time: req.body.DATE
      },
    })
    .then((response) => {
      // console.log(req.body.data)
      res.send(req.body);
      // console.log(response.data);
      console.log(22222);
    })
    .catch(function (error) {
      res.send(error);
      console.log(11111);
      console.log(error);
    });
});

// 물 먹었는지
router.post("/waterdrink", async function (req, res, next) {
  console.log(req.body)
  drink = req.body.DRINK
  res.json(req.body);

  await axios
    .post("http://127.0.0.1:8079/unauth/setModule", {
      module_id: 1,
      data: {
        drink: drink,
        water: water,
        time: req.body.DATE
      },
    })
    .then((response) => {
      // console.log(req.body.data)
      res.send(req.body);
      // console.log(response.data);
      console.log(22222);
    })
    .catch(function (error) {
      res.send(error);
      console.log(11111);
      console.log(error);
    });
});

// 물 부족한지
router.post("/waterlack", async function (req, res, next) {
  water = req.body.WATER_LACK
  res.json(req.body);
  await axios
    .post("http://127.0.0.1:8079/unauth/setModule", {
      module_id: 1,
      data: {
        drink: drink,
        water: water,
        time: req.body.DATE
      },
    })
    .then((response) => {
      // console.log(req.body.data)
      res.send(req.body);
      // console.log(response.data);
      console.log(22222);
    })
    .catch(function (error) {
      res.send(error);
      console.log(11111);
      console.log(error);
    });
});
router.post("/getAccessToken", function (req, res, next) {
  console.log(req.headers["x-access-token"]);
  axios
    .post("http://127.0.0.1:8079/unauth/getAccessToken", {
      email: req.body.email,
      pw: req.body.pw,
    })
    .then((response) => {
      res.send(response.data);
      console.log(response.data);
      console.log(22222);
    })
    .catch(function (error) {
      res.send(error);
      console.log(11111);
      console.log(error);
    });
});
router.post("/getSession", function (req, res, next) {
  console.log(req.headers["x-access-token"]);
  axios
    .post("http://127.0.0.1:8079/rpi/session", {
      serial: req.body.serial,
    })
    .then((response) => {
      res.send(response.data);
      console.log(response.data);
      console.log(22222);
    })
    .catch(function (error) {
      res.send(error);
      console.log(11111);
      console.log(error);
    });
});
router.post("/getModule", function (req, res, next) {
  console.log("1" + req.headers["x-access-token"]);
  axios
    .post("http://127.0.0.1:8079/auth/getModule", {
      module_id: req.body.module_id
    }, {
      headers: {
        "x-access-token": req.headers["x-access-token"]
      }
    })
    .then((response) => {
      res.send(response.data);
      console.log(response.data);
      console.log(22222);
    })
    .catch(function (error) {
      res.send(error);
      console.log(11111);
      console.log(error);
    });
});

router.post("/setModule", function (req, res, next) {
  axios
    .post("http://127.0.0.1:4500/unauth/setModule", {
      module_id: req.body.module_id,
      module_data: req.body.module_data,
    })
    .then((response) => {
      res.send(response.data);
    })
    .catch(function (error) {
      res.send(error);
      console.log(error);
    });
});

module.exports = router;
