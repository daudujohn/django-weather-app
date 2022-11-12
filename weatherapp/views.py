import os
from dotenv import load_dotenv
import datetime

from django.shortcuts import render
import requests

load_dotenv()
# Create your views here.
def index(request):
    if 'city' in request.POST:
        print(request.POST)
        city = request.POST['city']
    else: 
        city = 'London'
    API_KEY = os.getenv('API_KEY')
    URL = 'http://api.openweathermap.org/geo/1.0/direct'
    PARAMS = {'q': city, 'appid': API_KEY}
    r = requests.get(URL, PARAMS)
    res = r.json()
    lat = res[0]['lat']
    lon = res[0]['lon']

    URL = 'https://api.openweathermap.org/data/2.5/weather'
    PARAMS = {'lat': lat, 'lon': lon, 'appid': API_KEY, 'units': 'metric'}
    r = requests.get(url=URL, params=PARAMS)
    res = r.json()
    description = res['weather'][0]['description']
    icon = res['weather'][0]['icon']
    temp = res['main']['temp']
    day = datetime.date.today()
    context = {'description': description, 'icon': icon, 'temp': temp, 'day': day, 'city': city}
    return render(request, 'weatherapp/index.html', context)