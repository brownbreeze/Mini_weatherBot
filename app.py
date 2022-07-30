from flask import Flask, jsonify, request, Response
import json
import requests
import time
import os

app = Flask(__name__)

url = 'https://thirdparty-weather-api-v2.droom.workers.dev'

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

greeting_ment_list =[
    '폭설이 내리고 있어요.',
    '눈이 포슬포슬 내립니다.',
    '폭우가 내리고 있어요.',
    '비가 오고 있습니다.',
    '날씨가 약간은 칙칙해요.',
    '따사로운 햇살을 맞으세요.',
    '날이 참 춥네요.',
    '날씨가 참 맑습니다.'
]

headsup_ment_list=[
    '내일 폭설이 내릴 수도 있으니 외출시 주의하세요.',
    '눈이 내릴 예정이니 외출 시 주의하세요.',
    '폭우가 내릴 예정이에요. 우산을 미니 챙겨두세요.',
    '며칠동안 비 소식이 있어요.',
    '날씨는 대체로 평온할 예정이에요.'
]

@app.route('/')
def home():
    return jsonify(text='welcome~ ')

def elapsed_time(f):
    def wrapper(*args, **kwargs):
        st = time.time()
        v = f(*args, **kwargs)
        print(f"{f.__name__}: {time.time()-st}")
        return v
    return wrapper

def current(lat, lon, api_key):
    global url
    current_url = '/current'
    response = requests.get(url+current_url, params={"lat":lat,"lon":lon, "api_key":api_key})

    print(f'current : {response.content}')
    return [0, response.json()]

def forcast(lat, lon, hour_offset, api_key):
    global url
    forcast_url = '/forecast/hourly'
    response = requests.get(url + forcast_url, params={"lat": lat, "lon": lon, "hour_offset":hour_offset, "api_key": api_key})

    print(f'forcast {hour_offset}:{response.content}')
    return [hour_offset, response.json()]

def history(lat, lon, hour_offset, api_key):
    global url
    history_url = '/historical/hourly'
    response = requests.get(url + history_url, params={"lat": lat, "lon": lon, "hour_offset":hour_offset, "api_key": api_key})

    print(f'history {hour_offset}:{response.content}')
    return [hour_offset, response.json()]

def get_tempaerature_ment(idx, diff_temper, max_temp, min_temp):
    temperature_ment_list = [
        f'어제보다 {diff_temper}도 덜 덥습니다.',
        f'어제보다 {diff_temper}도 더 춥습니다.',
        f'어제보다 {diff_temper}도 더 덥습니다.',
        f'어제보다 {diff_temper}도 덜 춥습니다.',
        '어제와 비슷하게 덥습니다.',
        '어제와 비슷하게 춥습니다.'
    ]
    temperature_last_ment = f' 최고기온은 {max_temp}도, 최저기온은 {min_temp}도 입니다.'
    result = ''
    if idx != -1:
        result = temperature_ment_list[idx]
    result += temperature_last_ment
    return result

@elapsed_time
@app.route('/summary')
def summary(test = False):
    #api_key = 'CMRJW4WT7V3QA5AOIGPBC'
    api_key = get_apikey("Authorization")
    current_list = list()
    forcast_list = list()
    history_list = list()
    #for test
    if test is False:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
    else :
        lat = -13.3
        lon = 125

    if lat is None or lon is None:
        return Response(
            "Bad Request",
            status=400)
    elif float(lat) < -90.0 or float(lat) >= 90 :
        return Response(
            "Bad Request",
            status=400)
    elif float(lon) < -180.0 or float(lon) >= 180.0 :
        return Response(
            "Bad Request",
            status=400)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures_h = [executor.submit(history,lat,lon,t,api_key)
                   for t in range(-24,0,6)]
        futures_f = [executor.submit(forcast,lat,lon, t,api_key)
                   for t in range(6,50,6)]
        futures_c = [executor.submit(current,lat,lon, api_key)]

        for future in as_completed(futures_c):
            current_list.append(future.result())
        for future in as_completed(futures_h):
            history_list.append(future.result())
        for future in as_completed(futures_f):
            forcast_list.append(future.result())

    forcast_list.sort()
    history_list.sort()

    for histo in history_list:
        print(histo)
    for forc in forcast_list:
        print(forc)

    idx = 0
    diff_temper = 0

    # greeting
    greeting = ''
    current_value = current_list[0][1]
    if current_value["code"] == 3:
        idx = 0 if current_value["rain1h"] >= 100 else 1
    elif current_value["code"] == 2:
        idx = 2 if current_value["rain1h"] >= 100 else 3
    elif current_value["code"] == 1:
        idx = 4
    else:
        if current_value["temp"] >= 30:
            idx = 5
        elif current_value["temp"] <= 0:
            idx = 6
        else :
            idx = 7
    greeting = greeting_ment_list[idx] if idx in range(0,7) else 7
    print(greeting)

    # temperature
    idx = -1
    diff_temper= current_value["temp"]
    max_temp = current_value["temp"]
    min_temp = current_value["temp"]
    for hist in history_list:
        if hist[0] == -24:
            diff_temper -= hist[1]["temp"]
        if max_temp < hist[1]["temp"]:
            max_temp = hist[1]["temp"]
        if min_temp > hist[1]["temp"]:
            min_temp = hist[1]["temp"]
    print(f'diff : {diff_temper}, max : {max_temp}, min : {min_temp}')
    if diff_temper < 0 and current_value["temp"] >= 15:
        idx = 0
    elif diff_temper < 0 and current_value["temp"] < 15:
        idx = 1
    elif diff_temper > 0 and current_value["temp"] >= 15:
        idx = 2
    elif diff_temper > 0 and current_value["temp"] < 15:
        idx = 3
    elif diff_temper == 0 and current_value["temp"] >= 15:
        idx = 4
    elif diff_temper == 0 and current_value["temp"] < 15:
        idx = 5
    temperature = get_tempaerature_ment(idx, diff_temper, max_temp, min_temp)
    print(temperature)

    # heads_up
    heads_up = ''
    idx = -1
    forcast_code = current_value["code"]
    forcast_time = 1 if forcast_code == 3 else 0
    for forc in forcast_list:
        if forc[1]["code"] == 3:
            if forcast_code == 3 :
                forcast_time += 1
            forcast_code = 3
        else :
            forcast_time = 0
        if forcast_time >=3 and forcast_code == 3:
            if forc[0] <= 24:
                idx = 0
            else:
                idx = 1
            break
    else:
        forcast_code = current_value["code"]
        forcast_time = 1 if forcast_code == 2 else 0
        for forc in forcast_list:
            if forc[1]["code"] == 2:
                if forcast_code == 2:
                    forcast_time += 1
                forcast_code = 2
            else:
                forcast_time = 0
            if forcast_time >= 3 and forcast_code == 2:
                if forc[0] <= 24:
                    idx = 3
                else:
                    idx = 4
                break
        else:
            idx =5
    heads_up = headsup_ment_list[idx-1]
    print(heads_up)

    json_object = {
        "summary" :{
            "greeting":greeting,
            "temperature":temperature,
            "heads-up":heads_up
        }
    }
    return json.dumps(json_object, ensure_ascii=False)

def get_apikey(key_name, json_filename='secret.json'):
    # 해당 py파일의 속해 있는 폴더가 base_dir
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 해당 프로젝트 파일내 json파일이 있으므로 폴더패스와 파일이름을 합쳐 json_file의 절대경로값 얻는다
    json_filepath = os.path.join(BASE_DIR, json_filename)

    # json_file이 존재하지 않으면 error 발생
    if(not os.path.isfile(json_filepath)):
        print("JSON File Not Found")
        raise FileNotFoundError

    # json파일이 존재하면 json파일내의 모든 key, value값을 얻는다
    with open(json_filepath) as f:
        json_p = json.loads(f.read())
        print("json_p:  ", json_p)

    try:
        # key에 해당하는 value를 얻는다 ex. json_p["Authorization"]
        value=json_p[key_name]
        print(value)
        return value
    except KeyError:
        # 해당하는 key_name이 없는 경우이다
        error_msg = "ERROR: Unvalid Key"
        return error_msg