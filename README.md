# Mini_weatherBot
weather bot, flask, python, API

## Requirement 
- GET /summary
  - Request parm
    - param
      - lat (float) 위도 (-90<=x<90)
      - lon (float) 경도 (-180<=x<180)
    - Example
      - /summary?lat=-13.3&lon=125
  - Response
    - 200 OK
    - 400 Bad Request
    - 408 Reqeust timeout
    - 500 Internal Server Error 

## Usage
- development 상태
### 실행 
```bash
set FLASK_ENV=development
set FLASK_APP=app.py
flask run
```
### 테스트 
`http://127.0.0.1:5000/summary?lat=13.3&lon=124`

