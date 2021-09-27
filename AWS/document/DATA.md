### mongoDB

# Vuex
| date     | editor | desc        |
| -------- | ------ | ----------- |
| 21-07-05 | 김지환 | 초안        |
| 21-07-07 | 김지환 |             |
| 21-07-08 | 김지환 | 프론트 작성 |

### mainInfo.js
- state
  - robots [object]
    - id (String)
    - modules [object]
      - id (String)
      - type_id (String)
      - date (time)
      - module_data (Object)
      - clickable [Boolean]
  - cur (object]
    - robot_idx (Number)
    - module_idx (Number)

### userInfo.js
- state
  - host (String)
  - accessToken (String)
  - user_email (String)

# MongoDB
erlCloud
![image](./DATA.jpg)