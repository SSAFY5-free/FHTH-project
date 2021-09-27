'use strict';

module.exports = {
  up: (models, mongoose) => {
    return models["users"].create([
      {
        email: "aa@aa",
        pw: "aaa",
        robots_id: [1, 2]
      }
    ]).then(res => {
      console.log(res.insertedCount);
    });
  },

  down: (models, mongoose) => {
    return models["users"].deleteMany({}).then(res => {
      console.log(res.deletedCount);
    });
  }
};
