//https://www.npmjs.com/package/connect-mongodb-session
const express = require("express");
const session = require("express-session");
const MongoDBStore = require("connect-mongodb-session")(session);

//dotenv
const dotenv = require("dotenv").config({});
const env = process.env;

var store = new MongoDBStore({
  uri: env.mongo_HOST,
  databaseName: "fhth",
  expires: 1000 * 10,
  collection: "mySessions",
});

// Catch errors
store.on("error", function (error) {
  console.log(error);
});

module.exports = (app) => {
  app.use(
    require("express-session")({
      secret: "This is a secret",
      cookie: {
        maxAge: 1000 * 10, // 1 week
      },
      store: store,
      resave: true,
      saveUninitialized: true,
    })
  );
};
