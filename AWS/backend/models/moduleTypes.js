'use strict';
const autoIdSetter = require('../utils/auto-id-setter');
module.exports = mongoose => {
  const newSchema = new mongoose.Schema({
    name: {
      type: String
    }
  });
  autoIdSetter(newSchema, mongoose, 'moduleTypes', 'id');
  const moduleTypes = mongoose.model('moduleTypes', newSchema);
  return moduleTypes;
};