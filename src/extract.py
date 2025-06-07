import requests
from config import API_KEY, BASE_URL
import os

FAILED_LOG_PATH = os.path.join("logs", "failures.log")
os.makedirs("logs", exist_ok=True)

def extract_weather_data(cities):
    
    weather_data = []
    with open(FAILED_LOG_PATH, "w") as log_file:
        for city in cities:
            params = {
                "key": API_KEY,
                "q": city
            }
            try:
                response = requests.get(BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                weather_data.append({
                    "raw": data,
                    "city": city
                })
            
            except requests.RequestException as e:
                log_file.write(f"{city}\n")

    return weather_data
