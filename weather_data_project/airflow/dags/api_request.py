import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")

api_url = f"http://api.weatherstack.com/current?access_key={API_KEY}&query=Toronto"

def fetch_data():
    print("Fetching eeather data from Weatherstack API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API response received successfully.")
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise


# fetch_data()

def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'Toronto, Canada', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'Toronto', 'country': 'Canada', 'region': 'Ontario', 'lat': '43.667', 'lon': '-79.417', 'timezone_id': 'America/Toronto', 'localtime': '2026-03-23 18:23', 'localtime_epoch': 1774290180, 'utc_offset': '-4.0'}, 'current': {'observation_time': '10:23 PM', 'temperature': 2, 'weather_code': 122, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0004_black_low_cloud.png'], 'weather_descriptions': ['Overcast'], 'astro': {'sunrise': '07:16 AM', 'sunset': '07:34 PM', 'moonrise': '09:24 AM', 'moonset': '12:35 AM', 'moon_phase': 'Waxing Crescent', 'moon_illumination': 20}, 'air_quality': {'co': '239.85', 'no2': '14.55', 'o3': '79', 'so2': '6.05', 'pm2_5': '4.65', 'pm10': '5.15', 'us-epa-index': '1', 'gb-defra-index': '1'}, 'wind_speed': 27, 'wind_degree': 332, 'wind_dir': 'NNW', 'pressure': 1024, 'precip': 0, 'humidity': 51, 'cloudcover': 100, 'feelslike': -3, 'uv_index': 0, 'visibility': 14, 'is_day': 'yes'}}
