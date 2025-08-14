import requests
import json
import os

# Load config.json
with open("config.json", "r") as f:
    config = json.load(f)

# Get API key from config
API_KEY = config["jwt"]["secret_key"]

# Build the weather URL
WEATHER_URL = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Islamabad%2C%20Pakistan?unitGroup=us&key={API_KEY}&contentType=json"

def get_weather_forecast():
    response = requests.get(WEATHER_URL)
    response.raise_for_status()  # Raise error if request failed
    return response.json()
