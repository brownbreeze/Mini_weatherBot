# Mini_weatherBot
weather bot, flask, python, API

## Mini_weatherBot ? 
- 현재 날씨와 예보 정보를 종합하여 날씨 요약 문구를 생성해주는 HTTP API이다.
- 현재 날씨 또는 예보 정보는 외부 날씨 API 를 이용한다.
- 하지만, 해당 외부 날씨 API 는 최소 300ms 소요된다.
- 해당 API는 최대 소요시간 1500 msec 소요된다.

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

### 실행 
- gitlab 에서 소스 로드
- requirements 설치 
```bash
set FLASK_ENV=development
set FLASK_APP=app.py
flask run
```

### 테스트 
- API 호출
  - `http://127.0.0.1:5000/summary?lat=13.3&lon=124`
- pytest 이용
  - `pytest app_test.py --html=report/report.html --self-contained-html`

