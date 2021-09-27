# Rpi_backend

## INSTALL & START
    git clone -b Rpi --single-branch <repo URL>
    cd backend_rpi
    npm install
    npm start
  
## TEST
* POSTMAN
```  
POST http://localhost/pet/foodeat   - 음식 먹었는지 안먹었는지
POST http://localhost/pet/foodleft  - 음식이 얼마나 남았는지
POST http://localhost/pet/waterdrink  - 물을 마셨는지 안마셨는지
POST http://localhost/pet/waterlack  - 물이 부족한지 아닌지
```

## ISSUE
    FINDBYIDANDUPDATE 실행까지는 되는데 값이 업데이트 되지 않음 -> 찾아보니 저 구문 자체가 원래 기존 document를 반환한다함 좀더 찾아봐야 할듯
        
