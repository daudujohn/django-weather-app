import os
from os import path
from dotenv import load_dotenv
import datetime

from django.shortcuts import render
import requests

load_dotenv()

# TODO: Make timezones and date match the searched city
# TODO: Use the current location of the machine to display weather
# TODO: Replace static cities with 'most searched cities' and 'recently searched cities' only after signing in.

# Create your views here.
def index(request):
    user_location, user_town, state, city_view = '', '', '', ''
    city_count_dict = {}
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    if 'city' in request.POST and request.POST['city'].strip() != '':
        city = request.POST['city']
        city_view = city 
        # if city in city_count_dict:
        #     city_count_dict[city] += 1
        # else:
        #     city_count_dict[city] = 0
        print(f'\nUser City request: {request.POST}\n')
    else:
        CURRENT_LOCATION_API_KEY = os.getenv('CURRENT_LOCATION_API_KEY')
        URL = 'https://api.bigdatacloud.net/data/ip-geolocation'
        PARAMS = {'localityLanguage': 'en', 'key': CURRENT_LOCATION_API_KEY}
        r = requests.get(url=URL, params=PARAMS, headers=headers)
        res = r.json()
        state = res['location']["principalSubdivision"]
        user_town = res['location']['localityName']
        user_location = res['location']['localityName'].split('/')[-1]
        print(f'State: {state}, User_location: {user_location}, User_town: {user_town}')
        city = user_town
        city_view = f'{user_location}, {state}'

    try:
        API_KEY = os.getenv('API_KEY')
        URL = 'http://api.openweathermap.org/geo/1.0/direct'
        PARAMS = {'q': city, 'appid': API_KEY}
        r = requests.get(URL, PARAMS, headers=headers)
        res = r.json ()
        lat = res[0]['lat']
        lon = res[0]['lon']
    except IndexError:
        API_KEY = os.getenv('API_KEY')
        URL = 'http://api.openweathermap.org/geo/1.0/direct'
        city = state
        PARAMS = {'q': city, 'appid': API_KEY}
        r = requests.get(URL, PARAMS, headers=headers)
        res = r.json ()
        lat = res[0]['lat']
        lon = res[0]['lon']
    print()
    print(res)
    print()
    print(f"lat, lon of {city} = {lat, lon}")

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
    
    # Forecast
    URL = 'https://api.openweathermap.org/data/2.5/forecast'
    PARAMS = {'lat': lat, 'lon': lon, 'appid': API_KEY, 'units': 'metric'}
    r = requests.get(url=URL, params=PARAMS, headers=headers)
    res = r.json()
    print(f'STATUS CODE: {r.status_code}')
    forecast_dict = {}
    forecast_list = [
        forecast_dict.update(
            {i: [datetime.datetime.strptime(date['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime('%A'), 
                date['main']['temp'], 
                date['weather'][0]['description']]}) 
        for i, date in enumerate(res['list']) if '12:00:00' in date['dt_txt']]
    print(f'\n{forecast_dict}\n')
    del forecast_list
    #  weekday, temp, description
    context = {
         'description': description,
         'temp': temp,
         'humidity': humidity,
         'wind_speed': wind_speed, 
         'clouds': clouds,
         'weekday': weekday,
         'month': month,
         'day': day,
         'city': city_view, 
         'hour': hour,
         'minute': minute, 
         'meridiem': meridiem,
         'meridiem_folder': meridiem_folder,
         'background_path': background_path,
         'forecast_dict': forecast_dict,
         
        }
    return render(request, 'weatherapp/index.html', context)
