const moment = require("moment")
'use strict';
module.exports = {
  up: async (models, mongoose) => {
    /*
    dev1
    isEaten
    timeEaten
    numEaten

    dev2
    timeWater
    isWater
    */
    await models["registedModules"].create(
      {
        serial: "970121",
        type_id: 1,
        data: { isEaten: false, timeEaten: moment().format(), numEaten: 30, timeWater: null, isWater: null },
        // reservation: [moment().add(1, "day"), moment().add(1, "minute")],
        reservation: moment(),
        name: "module1"
      })
    await models["registedModules"].create({
      serial: "970232",
      type_id: 2,
      data: { isEaten: null, timeEaten: null, numEaten: null, timeWater: moment().format(), isWater: true },
      // reservation: [moment().add(1, "day"), moment().add(1, "minute")],
      name: "module2"
    })
    return await models["registedModules"].create(
      {
        serial: "970343",
        type_id: 1,
        data: { isEaten: true, timeEaten: moment().format(), numEaten: 90, timeWater: null, isWater: null },
        // reservation: [moment().add(1, "day"), moment().add(1, "minute")],
        reservation: moment(),
        name: "module3"
      }
    ).then((res) => {
      console.log()
    })
  },

  down: (models, mongoose) => {
    return models["registedModules"].deleteMany({}).then(res => {
      console.log(res.deletedCount);
    });
  }
};
