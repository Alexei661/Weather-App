import urllib.request
import json
import os
from dotenv import load_dotenv
import time
from typing import Dict, Any
load_dotenv()
# Function to fetch weather data
def fetch_weather_from_api(city: str, api_key: str):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    complete_url = f"{base_url}{city}?unitGroup=metric&contentType=json&key={api_key}"

    try:
        with urllib.request.urlopen(complete_url) as response:
            data = response.read()
            json_data = json.loads(data)
            return json_data  # ← RETURNS here
    except Exception as e:
        print(f"API error: {e}")
        return None


# Replace with your API key
api_key = os.getenv("Weather_API")
# Specify the city
city = 'Timisoara'


def print_weather(json_data):
    if not json_data:
        print("No data")
        return
    print("Weather data for:", json_data['address'])
    for day in json_data['days']:
        print(f"Date: {day['datetime']}, Temperature: {day['temp']}°C, Conditions: {day['conditions']}")


data1=fetch_weather_from_api(city, api_key)
print_weather(data1)

