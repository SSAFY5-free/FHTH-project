# Frontend
```
/App
├── /Login
├── /Signup
│   └── /addRobot
│
└── /Main
│   ├── Robot
│   ├── Module
│   └── ModuleView
```
# Backend
/route/index
```
├── /unauth
│   ├── /addAccount => {result : 0 / 1}
│   ├── /getAccessToken => {accessToken : accessToken / ""}
│   ├── /verifyRobot => {result : 0 / 1}
│   └── /setModule {module} => {}
│   
├── /auth
│   ├── /getRobots {} => {robot}
│   └── /getModules {robot_id} => {registedModule} 
│   
│    
├── /admin
│   ├── /addModuleType {result : 1}
│   ├── /addRegistedModule {result : 1}
│   ├── /addAccount {result : 1}
│   └── /addRobots {result : 1}
```
