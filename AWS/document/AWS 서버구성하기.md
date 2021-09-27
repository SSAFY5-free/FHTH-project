# mongo DB
1. mongo
   1. 설치
      1. 전에 깔아놨음
   2. 설정
      1. mongod를 실행해서 백그라운드에서 동작하도록 해야함.
         1. 보안설정이 있음. mongod --bind_ip 127.0.0.1 
         2. https://docs.mongodb.com/manual/core/security-mongodb-configuration/
   3. db 내용 가져오기
      1. mongodump를 사용해서 데이터들을 가져올 수 있음.
      2. mongo datatools에 포함되어있음.
         1. https://www.mongodb.com/try/download/database-tools?tck=docs_databasetools
         2. 사용법
            1. https://webisfree.com/2020-08-20/[mongodb]-%EB%AA%BD%EA%B3%A0db-mongodump-%EA%B7%B8%EB%A6%AC%EA%B3%A0-mongorestore-%EC%82%AC%EC%9A%A9%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95
2. 깃 가져오기
   1. git remote -a로 원격저장소의 브랜치 종류 확인
   2. git pull origin AWS 로 원격 저장소의 브랜치 가져오기
3. backend 구성하기
   1. backend에서 npm install 로 의존성 파일 다운