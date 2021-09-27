const express = require("express");
const app = express();
const routes = require("./routes");
const env = process.env;
require("dotenv").config({});

//middleware
const cors = require("cors");
var whitelist = ["http://127.0.0.1:8081", "http://127.0.0.1:8080", "http://127.0.0.1:8079"];
var corsOptions = {
  origin: function (origin, callback) {
    // if (whitelist.indexOf(origin) !== -1) {
      callback(null, true);
    // } else {
      // callback(new Error("Not allowed by CORS"));
    // }
  },
};

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cors(corsOptions));
app.use("/", routes);


const http_server = require("http").createServer(app);
const https_server = require("https").createServer(
  {
    //  ca: fs.readFileSync('/fullchain.pem'),
    //  key: fs.readFileSync('/privkey.pem'),
    //  cert: fs.readFileSync('/cert.pem')
  },
  app
);

//socket.io
require("./utils/socket.js").createSocket(http_server, https_server);

//server listen
http_server.listen(env.HTTP_PORT, "0.0.0.0", function () {
  console.log(env.HTTP_PORT + " / FHTH.server is running");
});

https_server.listen(env.HTTPS_PORT, "::", function () {
  console.log(env.HTTPS_PORT + " / FHTH.server2 is running");
});
