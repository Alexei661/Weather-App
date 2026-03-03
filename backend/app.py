import urllib.request
import json
import os
from dotenv import load_dotenv
load_dotenv()
# Function to fetch weather data
def fetch_weather(city, api_key):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    complete_url = f"{base_url}{city}?unitGroup=metric&contentType=json&key={api_key}"
    try:
        with urllib.request.urlopen(complete_url) as response:
            data = response.read()
            # Parse JSON data
            json_data = json.loads(data)
            print("Weather data for:", json_data['address'])
            for day in json_data['days']:
                print(f"Date: {day['datetime']}, Temperature: {day['temp']}°C, Conditions: {day['conditions']}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}, {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")

# Replace with your API key
api_key = os.getenv("Weather_API")
# Specify the city
city = 'Timisoara'

# Call function to fetch weather data
fetch_weather(city, api_key)