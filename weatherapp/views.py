import os
from os import path
from dotenv import load_dotenv
import datetime

from django.shortcuts import render
import requests

load_dotenv()

# TODO: Make timezones and date match the searched city
# TODO: Use the current location of the machine to display weather

# Create your views here.
def index(request):
    CURRENT_LOCATION_API_KEY = os.getenv('CURRENT_LOCATION_API_KEY')
    URL = 'https://api.bigdatacloud.net/data/ip-geolocation'
    PARAMS = {'localityLanguage': 'en', 'key': CURRENT_LOCATION_API_KEY}
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    r = requests.get(url=URL, params=PARAMS, headers=headers)
    res = r.json()    
    state = res['location']["principalSubdivision"]
    user_town = res['location']['localityName']
    user_location = res['location']['localityName'].split('/')[-1]
    print(f'State: {state}, User_location: {user_location}')
    
    if 'city' in request.POST:
        city = request.POST['city']
        print(f'\nUser City request: {request.POST}\n')
    else:
        print(user_town, type(user_town))
        city = user_town
        print(f'\nDefault City request: {request.POST}\n')

    API_KEY = os.getenv('API_KEY')
    URL = 'http://api.openweathermap.org/geo/1.0/direct'
    PARAMS = {'q': city, 'appid': API_KEY}
    r = requests.get(URL, PARAMS, headers=headers)
    res = r.json ()
    print()
    print(res)
    print()
    lat = res['location']['latitude']
    lon = res['location']['longitude']
    print(f"lat, lon = {lat, lon}")

    URL = 'https://api.openweathermap.org/data/2.5/weather'
    PARAMS = {'lat': lat, 'lon': lon, 'appid': API_KEY, 'units': 'metric'}
    r = requests.get(url=URL, params=PARAMS, headers=headers)
    res = r.json()
    description = res['weather'][0]['description']
    temp = res['main']['temp']
    humidity = res['main']['humidity']
    wind_speed = res['wind']['speed']
    clouds = res['clouds']['all']

    TIMEZONE_API_KEY = os.getenv('TIMEZONE_API_KEY')
    URL = 'https://timezone.abstractapi.com/v1/current_time'
    PARAMS = {'api_key': TIMEZONE_API_KEY, 'location': f'{lat}, {lon}'}
    r = requests.get(url=URL, params=PARAMS, headers=headers)
    res = r.json()
    print(f"date: {res['datetime']}")

    api_datetime = datetime.datetime.strptime(res['datetime'], "%Y-%m-%d %H:%M:%S")
    weekday = api_datetime.strftime('%A')
    month = api_datetime.strftime('%h')
    day = api_datetime.strftime('%d')
    hour = api_datetime.strftime('%I')
    minute = api_datetime.strftime('%M')
    meridiem = 'am' if (api_datetime.hour < 12) else 'pm'
    meridiem_folder = 'day' if (meridiem == 'am' or api_datetime.hour < 17) else 'night'
    print(meridiem, meridiem_folder)

    def background_change():
        previous_description = ''
    background_path = f'images/{meridiem_folder}/{description.replace(" ", "_")}.jpg'
    
    context = {
         'description': description,
         'temp': temp,
         'humidity': humidity,
         'wind_speed': wind_speed, 
         'clouds': clouds,
         'weekday': weekday,
         'month': month,
         'day': day,
         'city': f'{user_location}, {state}' if city not in request.POST else city, 
         'hour': hour,
         'minute': minute, 
         'meridiem': meridiem,
         'meridiem_folder': meridiem_folder,
         'background_path': background_path,
        }
    return render(request, 'weatherapp/index.html', context)

def signup(request):
    pass