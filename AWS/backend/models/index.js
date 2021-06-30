const mongoose = require('mongoose')
//User
const userDeviceSchema = new mongoose.Schema({
    type : Number,
    serial : String, 
 })
 const userSchema = new mongoose.Schema({
    email : String,
    pw : String,
    device : [userDeviceSchema]
 })
const statusDev1 = new mongoose.Schema({
   power : String,
   remain : Number
})
//Device
const deviceSchema = new mongoose.Schema({
   type : String
})

const registedDeviceSchema = new mongoose.Schema({
   type : String,
   serial : String,
   status : {}
})

const sessionSchema = new mongoose.Schema( {
   sid : String,
   email : String,
})
const User = mongoose.model("User",userSchema)
const Device = mongoose.model("Device", deviceSchema) 
const RegistedDevice = mongoose.model("RegistedDevice", registedDeviceSchema)
const Session = mongoose.model = mongoose.model("Session", sessionSchema)
Session.createIndexes({
   createdAt : new Date(),
   expireAfterSeconds : 60*60 
})
 module.exports = {User, Device, RegistedDevice, Session}