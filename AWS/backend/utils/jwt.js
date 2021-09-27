//utils의 내용들을 구성.
// 암호화를 위한 bcrypt
// jwt(jsonWebToken) {
//     https://jwt.io/ 
//     회원 정보 인증시 사용
//     header(header).payload(내용).서명(signature)
//     인코딩값을 합친후 비밀키를 통해 암호화해서 생성
    
//     header
//     typ - 토큰의 타입
//     alg - 해싱 알고리즘
//     payload - 토큰에 담을 정보
//     signature - header의 인코딩값 + payload의 
    
// }

const jwt = require("jsonwebtoken");

const verifyToken = (req, res, next) => {
    try {
        console.log("get session try : " , req.headers)
        //보통 jwt는 요청을 request의 header(authorization)에 보낸다;
        req.decoded = jwt.verify(req.headers.authorization, "fhth")
        console.log("decoded : " , req.decoded)
        return next();
    } catch (e) {
        return res.json(e);
    }
}

module.exports = {verifyToken}