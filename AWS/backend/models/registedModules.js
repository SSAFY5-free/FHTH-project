'use strict';
const autoIdSetter = require('../utils/auto-id-setter');
module.exports = mongoose => {
  const newSchema = new mongoose.Schema({
    serial: String,
    type_id: Number,
    data: mongoose.Schema.Types.Mixed,
    reservation: Date,
    actions: [],
    name: String
    ,
  }, {
    timestamps: true
  })
  autoIdSetter(newSchema, mongoose, 'registedModules', 'id');
  const registedModules = mongoose.model('registedModules', newSchema);
  return registedModules;
};