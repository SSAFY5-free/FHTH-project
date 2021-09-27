'use strict';
const autoIdSetter = require('../utils/auto-id-setter');
module.exports = mongoose => {
  const newSchema = new mongoose.Schema({
    email: String,
    pw: String,
    robots_id: [Number]
  })
  autoIdSetter(newSchema, mongoose, 'users', 'id');
  const users = mongoose.model('users', newSchema);
  return users;
};