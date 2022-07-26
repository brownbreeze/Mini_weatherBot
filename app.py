from flask import Flask, jsonify, request
import json
import requests
import time


app = Flask(__name__)

url = 'https://thirdparty-weather-api-v2.droom.workers.dev'

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

    print(response.status_code)
    print(response.content)
    pass

def forcast(lat, lon, hour_offset, api_key):
    global url
    forcast_url = '/forecast/hourly'
    response = requests.get(url + forcast_url, params={"lat": lat, "lon": lon, "hour_offset":hour_offset, "api_key": api_key})

    print(response.status_code)
    print(response.content)
    pass

def history(lat, lon, hour_offset, api_key):
    global url
    history_url = '/historical/hourly'
    response = requests.get(url + history_url, params={"lat": lat, "lon": lon, "hour_offset":hour_offset, "api_key": api_key})

    print(response.status_code)
    print(response.content)
    pass

@elapsed_time
@app.route('/summary')
def summary(test = False):

    #for test
    if test is False:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
    else :
        lat = 10
        lon = 3
    api_key = 'CMRJW4WT7V3QA5AOIGPBC'


    if lat is None or lon is None:
        lat = 10
        lon = 3
        #return '400 error'

    print(f'현재')
    current(lat, lon, api_key)
    greeting = ''

    print(f'과거')
    for t in range(-24,0,6):
        history(lat, lon, t, api_key)
        print(f'> {t} 전 과거')
    temperature = ''

    print(f'미래')
    for t in range(6,50,6):
        forcast(lat, lon, t, api_key)
        print(f'> {t} 후 미래')
    heads_up = ''

    json_object = {
        "summary" :{
            "greeting":greeting,
            "temperature":temperature,
            "heads-up":heads_up
        }
    }
    return json.dumps(json_object)
    #return jsonify(text='hello world!?', count = 0)