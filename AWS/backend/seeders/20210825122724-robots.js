'use strict';

module.exports = {
  up: async (models, mongoose) => {
    return await models["robots"].create([
      {
        serial: "123123",
        modules_id: [1, 2],
        name: "robot1",
        ip: ""
      },
      {
        serial: "212212",
        modules_id: [3],
        name: "robot2",
        ip: ""
      }
    ]).then(res => {
      console.log(res.insertedCount);
    });
  },

  down: (models, mongoose) => {
    return models["robots"].deleteMany({}).then(res => {
      console.log(res.deletedCount);
    });
  }
};
