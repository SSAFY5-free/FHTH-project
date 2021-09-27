// const dotenv = require("dotenv").config({});
// const env = process.env;

// module.exports = () => {
//   const mongoose = require("mongoose");
//   mongoose.connect(env.MONGO_HOST, {
//     useNewUrlParser: true,
//     useUnifiedTopology: true,
//     dbName: env.MONGO_DB,
//   });
//   const db = mongoose.connection;
//   db.on("error", console.error.bind(console, "connection error"));
//   db.once("open", () => {
//     console.log("mongoDB connected");
//   });
// };
