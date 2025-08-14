import requests

WEATHER_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Islamabad%2C%20Pakistan?unitGroup=us&key=F8769SZHLNAKEZC38S8J9LYR5&contentType=json"

def get_weather_forecast():
    response = requests.get(WEATHER_URL)
    return response.json()
