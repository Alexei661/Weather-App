import urllib.request
import json
import os
from dotenv import load_dotenv
import time
import redis
load_dotenv()

# Initialize Redis client
# Ensure you have REDIS_HOST, REDIS_PORT, and REDIS_PASSWORD in your .env file
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True
)

# Test connection immediately to catch config errors early
try:
    redis_client.ping()
    print(f"Successfully connected to Redis at {os.getenv('REDIS_HOST')}")
except redis.ConnectionError as e:
    print(f"Warning: Could not connect to Redis. Check credentials. Error: {e}")

# Function to fetch weather data
def fetch_weather_from_api(city: str, api_key: str):
    # Check Redis cache first
    cache_key = f"weather:{city.lower()}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print(f"Cache hit: Returning {city} weather from Redis.")
        return json.loads(cached_data)

    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    complete_url = f"{base_url}{city}?unitGroup=metric&contentType=json&key={api_key}"

    try:
        with urllib.request.urlopen(complete_url) as response:
            data = response.read()
            json_data = json.loads(data)
            # Cache the result in Redis for 1 hour (3600 seconds)
            redis_client.setex(cache_key, 3600, json.dumps(json_data))
            return json_data  # ← RETURNS here
    except Exception as e:
        print(f"API error: {e}")
        return None


# Replace with your API key
api_key = os.getenv("Weather_API")
# Specify the city
city = 'London'


def print_weather(json_data):
    if not json_data:
        print("No data")
        return
    print("Weather data for:", json_data['address'])
    for day in json_data['days']:
        print(f"Date: {day['datetime']}, Temperature: {day['temp']}°C, Conditions: {day['conditions']}")


data1=fetch_weather_from_api(city, api_key)
print_weather(data1)
