const express = require("express")
const router = express.Router()
const path = require("path")
const jwt = require('jsonwebtoken')
const {verifyToken} =require("../../utils/jwt")
const {User, Device } = require("../../models/index")

require("dotenv").config({
    path : path.resolve(
        process.cwd(),
        ".env"
        )
    })
    
const {MONGO_URI} = process.env

// router.get("/device", async (req, res) => {
//     //전체 device종류 목록 가져오기
//     Device.find({}, "type", (err,e) => {
//         res.send({"data" : e.reduce((acc,cur) => {
//             acc.push(cur["type"])
//             return acc
//         }, [])})
//     })
// })

// router.get("/device/add/:type", async (req, res) => {
//     //device 종류 추가
//     Device.create({type:req.params.type})
//     res.send({"data" : 1})
// })

router.post("/login", async (req, res) => {
    console.log(req.headers)
    // todo 세션 설정 수정
    const {email, pw, } = req.body
    const result = await User.findOne({email, pw})

    //로그인 실패 : 존재하지 않는 회원
    if(!result) return res.json({statusCode:404});
    //로그인 성공 => 세션 발급

    //todo refreshToken
    // const refreshToken = jwt.sign( {
    //     email
    // }, "fhth", {
    //     expiresIn:"24h"
    // })   
    const accessToken = jwt.sign( {
        email
    }, "fhth", {
        expiresIn:"1h"
    })   
    return res.json({
        statusCode : 200,
        auth_info : {
            accessToken//, refreshToken
        },
        email,
    });
})

router.post("/signup", async(req,res) => {
    //todo 암호화 미들웨어 추가
    //todo email이 중복되는지 확인
    const {email, pw, device} = req.body
    User.create({
       email, pw , device
    }, function (err) {
       console.log(err)
    })
    res.send({"result" : 1})
})

// router.post("/session", verifyToken, (req,res) => {
//     res.json(req.decoded)
// })
router.post("/devices", verifyToken, async (req,res) => {
    const email = req.decoded.email
    const result = await User.findOne({email})
    res.json({data : result.device})
})
module.exports = router