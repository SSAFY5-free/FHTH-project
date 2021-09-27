const db = require("../models").default;
exports.post_session = (req) => {
  return new Promise(async (resolve, reject) => {
    req.session.msg = "msg";
    console.log(req);
    const host = req.headers["x-forwarded-for"] || req.connection.remoteAddress;

    const { serial } = req.body;
    if (!serial) resolve({ err: "no data" });

    // Session.create({ host, serial });
    resolve();
  });
};
// exports.get_session = (data) => {
//   return new Promise(async (resolve, reject) => {
//     resolve();
//   });
// };
