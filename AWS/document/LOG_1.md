# Purpose 
 기록으로 남겨 같은 내용 반복하지 않도록하기.

### 21-07-06
1. [update] Front directory map
   1. >
      /App
   ├── /Login
   ├── /Signup
   │   └── /addRobot
   │
   └── /Main
   │   ├── **SideBar**
   │   ├── **Modules**
   │   ├──     └──**Modal**
   │   └── **NavBar**
   >
2. [try] Front SCSS
   1. ref
      1. https://poiemaweb.com/sass-basics
   2. how
      1. use node-module sass
      2. npm script : css
      3. import "./assets/css/all.css"
3. [create] document structure
   1. create dir in /document/ [doc, movie, ppt, update]
   2. create md
      1. SITEMAP
      2. DATA
      3. LOG_1
         1. plz ref /doumcnet/README.MD
4. [Do] Robot 컴포넌트에서 현재 선택된 로봇 데이터 가져오기
   1. userInfo에서 robots_id 데이터 접근하기
   2. robot_idx 인덱스의 robots_id 원소값 가져오기