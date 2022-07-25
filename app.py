from flask import Flask, jsonify, request
import json
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(text='welcome~ ')

@app.route('/summary')
def summary():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    api_key = 'CMRJW4WT7V3QA5AOIGPBC'
    url = 'https://thirdparty-weather-api-v2.droom.workers.dev'

    current_url = '/current'
    forcast_url = '/forecast/hourly'
    history_url = '/historical/hourly'

    response = requests.get(url+current_url, params={"lat":lat,"lon":lon, "api_key":api_key})

    print(f'현재')
    print(response.status_code)
    print(response.content)
    greeting = ''
    print(f'과거')
    for time in range(-24,0,6):
        response = requests.get(url + history_url, params={"lat": lat, "lon": lon, "hour_offset":time, "api_key": api_key})
        print(f'> {time} 전 과거')
        print(response.status_code)
        print(response.content)
    temperature = ''
    print(f'미래')
    for time in range(6,50,6):
        response = requests.get(url + forcast_url, params={"lat": lat, "lon": lon, "hour_offset":time, "api_key": api_key})
        print(f'> {time} 후 미래')
        print(response.status_code)
        print(response.content)
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