import os
import logging
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import API_KEY, BASE_URL
import multiprocessing

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/weather_fetch.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
session = requests.Session()

def fetch_with_retries(city, retries=2, delay=2,session=session):
    for attempt in range(1, retries + 1):
        try:
            response = session.get(BASE_URL, params={"key": API_KEY, "q": city}, timeout=10)
            response.raise_for_status()
            logging.info(f"Successfully fetched data for {city}")
            return response.json()
        except requests.RequestException as e:
            logging.warning(f"Attempt {attempt} failed for {city}: {e}")
            if attempt == retries:
                logging.error(f"All retries failed for {city}")
                return None
            time.sleep(delay)

def extract_weather_data(cities):
    weather_data = []
    max_workers = min(32, (multiprocessing.cpu_count() or 1) * 5)
    with ThreadPoolExecutor(max_workers) as executor:
        future_to_city = {executor.submit(fetch_with_retries, city): city for city in cities}
        for future in as_completed(future_to_city):
            city = future_to_city[future]
            try:
                data = future.result()
                if data:
                    weather_data.append({"raw": data, "city": city})
            except Exception as e:
                logging.error(f"Unexpected error for {city}: {e}")

    return weather_data
