'use strict';

module.exports = {
  up: async (models, mongoose) => {
    await models["moduleTypes"].create(
      {
        name: "급식기"
      })
    return await models["moduleTypes"].create({
      name: "급수기"
    })
  },

  down: (models, mongoose) => {
    return models["moduleTypes"].deleteMany({}).then(res => {
      console.log(res.deletedCount);
    });
  }
};
