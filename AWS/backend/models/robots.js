'use strict';
const autoIdSetter = require('../utils/auto-id-setter');
module.exports = mongoose => {
  const newSchema = new mongoose.Schema({
    serial: String,
    modules_id: [Number],
    name: String,
    ip: String,
  })
  autoIdSetter(newSchema, mongoose, 'robots', 'id');
  const robots = mongoose.model('robots', newSchema);
  return robots;
};