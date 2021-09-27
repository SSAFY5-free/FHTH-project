'use strict';

module.exports = {
  up: (models, mongoose) => {
    return models["counters"].create([
      {
      }
    ]).then(res => {
      console.log(res.insertedCount);
    });
  },

  down: (models, mongoose) => {
    return models["counters"].deleteMany({}).then(res => {
      console.log(res.deletedCount);
    });
  }
};
