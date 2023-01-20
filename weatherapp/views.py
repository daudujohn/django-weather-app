import os
from os import path
from dotenv import load_dotenv
import datetime
import weatherapp.getWeather

from django.shortcuts import render
import requests

load_dotenv()

# TODO: Make timezones and date match the searched city
# TODO: Use the current location of the machine to display weather
# TODO: Replace static cities with 'most searched cities' and 'recently searched cities' only after signing in.


# Create your views here.
def index(request):
    context = weatherapp.getWeather.getWeather(request)
    return render(request, 'weatherapp/index.html', context)