const { robotAPI } = require("../utils/axios")
const db = require("../models").default

module.exports.createSocket = function (http_server, https_server) {
  const io = require("socket.io")(http_server, {
    cors: {
      origin: [
        //! origin 상관없이 처리되도록 
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8281",
        "http://ssafy5-free.github.io",
        "https://ssafy5-free.github.io",
      ],

      methods: ["GET", "POST"],
      allowedHeaders: ["my-custom-header"],
      transports: ["websocket", "polling"],
      credentials: true,
    },
    allowEIO3: true,
  });
  io.attach(https_server, {
    cors: {
      origin: [
        "http://127.0.0.1:8081",
        "http://127.0.0.1:8281",
        "http://ssafy5-free.github.io",
        "https://ssafy5-free.github.io",
      ],

      methods: ["GET", "POST"],
      allowedHeaders: ["my-custom-header"],
      transports: ["websocket", "polling"],
      credentials: true,
    },
    allowEIO3: true,
  });
  io.on("connection", async (socket) => {
    console.log("Connect from Client: " + socket);
    //Registedmodule에 있는 id들 조회
    socket.on("module", async (data) => {
      const { id } = data;
      const result = await db["registedModules"].findOne({ id });
      socket.emit("module", {
        data: result.data,
      });

      // console.log("socket module : ", result);
    }),
      socket.on("command", async (msg) => {
        const { data } = msg
        console.log("command : ", msg);
        const { robot_id, direction } = msg
        const { ip } = await db["robots"].findOne({ id: robot_id })


        const payload = { command: "move", payload: direction }
        await robotAPI.sendMoveCmd(ip, payload).catch((error) => {
          console.log("jbjbjbjb: ", error)
        })
      });

  });
};
