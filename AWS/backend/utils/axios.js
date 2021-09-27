const axios = require("axios")
const dotenv = require("dotenv")
dotenv.config({})


// 로직 1. Axios 인스턴스 생성
//      https://axios-http.com/docs/instance
const request = axios.create({
    timeout: 2000
})

// 로직 2. Axios intercept로 핸들링 처리
//  try/catch 전에 핸들링 처리.
//  https://axios-http.com/docs/interceptors
//  https://velog.io/@pandati0710/axios-intercepter%EB%A1%9C-error-handling-%ED%95%98%EA%B8%B0
request.interceptors.response.use(function (response) {
    return response;
}, function (error) {
    // 로직 1. error 종료 분류
    //  https://coding8.tistory.com/6

    const { code } = error
    let msg, status = 500
    switch (code) {
        case "ECONNREFUSED":
            msg = "로봇의 네트워크 포트가 개방되어있지 않습니다"
            break
        case "EAI_AGAIN":
            msg = "IP가 설정되어있지 않습니다"
            break
        default:
            msg = "UnKnown Problem"
            break
    }
    // 로직 2. reject 실행
    return Promise.reject(msg);
});


// 로직 3. 관련 API 생성
module.exports.robotAPI = {
    port: 3000,
    //로직 2-1. 모듈 제어 커맨드 전송
    sendModuleCmd: async (robot_ip, payload) => {

        // 로직 1. url + path = 로봇 ip 주소
        const domain = "http://172.30.1.7:3000"
        const path = "/pet/servefood"
        const url = domain + path

        await request.post(url, payload
        ).then((data) => {
            console.log(`[Success] sendModuleCmd ${data}`)
        }).catch((error) => {
            console.log(`[Error] sendModuleCmd ${error}`)
            throw new Error(error)
        })
    },
    sendModuleAmount: async (robot_ip, payload) => {

        // 로직 1. url + path = 로봇 ip 주소
        const domain = "http://172.30.1.7:3000"
        const path = "/pet/feedcontrol"
        const url = domain + path

        await request.post(url + path, payload
        ).then((data) => {
            // console.log(`[Success] sendModuleCmd ${url}`)
        }).catch((error) => {
            // console.log(`[Error] sendModuleCmd ${url}`)
            throw new Error(error)
        })
    },
    //todo 로직 2-2.로봇 이동 커맨드 전송
    sendMoveCmd: async (robot_ip, payload) => {

        // 로직 1. url + path = 로봇 ip 주소
        const domain = "http://172.30.1.7:3000"
        const path = "/pet/control"
        const url = domain + path

        await request.post(url, payload
        ).then((data) => {
            console.log(`[Success] sendMoveCmd ${url}`)
        }).catch((error) => {
            console.log(`[Error] sendMoveCmd ${url}`)
            throw new Error(error)
        })
    }
}