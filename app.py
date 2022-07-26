from flask import Flask, jsonify, request
import json
import requests
import time


app = Flask(__name__)

url = 'https://thirdparty-weather-api-v2.droom.workers.dev'

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

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
    api_key = 'CMRJW4WT7V3QA5AOIGPBC'

    #for test
    if test is False:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
    else :
        lat = 10
        lon = 3

    # if lat is None or lon is None:
        #return '400 error'

    print(f'과거')
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures_h = [executor.submit(history,lat,lon,t,api_key)
                   for t in range(-24,0,6)]
        futures_f = [executor.submit(forcast,lat,lon, t,api_key)
                   for t in range(6,50,6)]
        futures_c = [executor.submit(current,lat,lon, api_key)]
        for future in as_completed(futures_c):
            print(future.result())
        for future in as_completed(futures_h):
            print(future.result())
        for future in as_completed(futures_f):
            print(future.result())

    greeting = ''
    temperature = ''
    heads_up = ''

    json_object = {
        "summary" :{
            "greeting":greeting,
            "temperature":temperature,
            "heads-up":heads_up
        }
    }
    return json.dumps(json_object)