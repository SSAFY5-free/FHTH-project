# 기술 스택
 - nodejs
 - mongoDB

# Run
```
1. cd /FHTH_FREE/AWS/backend </br>
2. nodemon
```

# Directory
/
├── /unauth
│   ├── /addAccount => {result : 0 / 1}
│   ├── /getAccessToken => {accessToken : accessToken / ""}
│   ├── ~~/getDevices => {data : [type]}~~
│   ├── ~~/verifyRegistedDevice => {result : 0 / 1}~~
│   ├── /verifyRobot => {result : 0 / 1}
│   └── ~~/verifyEmail~~
├── /auth
│   ├── ~~/setAccount~~
│   ├── ~~/setRegistedDeviceStatus~~
│   ├── **/getRobots** {} => {robots}
│   ├── **/getModules** {robot_id} => {registedModule} 
│   └── ~~/mainInfo [{serial, type, status = {}}]~~
├── /admin
│   ├── /addModuleType {result : 1}
│   ├── /addRegistedModule {result : 1}
│   ├── /addAccount {result : 1}
│   └── /addRobots {result : 1}



