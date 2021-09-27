const express = require("express")
const router = express.Router()
const path = require("path")

const jwt = require('jsonwebtoken')
const {verifyToken} =require("../utils/jwt")

const {User, Device, RegistedDevice } = require("../models/index")

require("dotenv").config({
    path : path.resolve(
        process.cwd(),
        ".env"
        )
    })
    
const {MONGO_URI} = process.env

//전체 device 목록 가져오기
router.get("/", async (req, res) => {
    Device.find({}, "type", (err,e) => {
        res.send({"data" : e.reduce((acc,cur) => {
            acc.push(cur["type"])
            return acc
        }, [])})
    })
})

//device 종류 추가
router.get("/add/:type", async (req, res) => {
    Device.create({type:req.params.type})
    res.send({"data" : 1})
})

router.post("/validation/registedDevice", async (req, res) => {
    console.log(req.body)
    const {serial, type} = req.body;
    const result = await RegistedDevice.findOne({serial, type})
    // console.log(result)

    if(!result) res.json({data:0})
    else res.json({data:1})
    return
})

module.exports = router