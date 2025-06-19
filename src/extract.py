import os,sys
import logging
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import API_KEY, BASE_URL
import multiprocessing

# Only set up logging if running as standalone script (not inside Airflow)
if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename='logs/weather_fetch.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Reuse requests session
session = requests.Session()

def fetch_with_retries(city, retries=2, delay=2, session=session):
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

    if not API_KEY:
        logging.error("No OPENWEATHER API_KEY configured! Exiting.")
        sys.exit(1)

    logging.info(f"Using API key: {API_KEY[:4]}… for extraction")
    logging.info(f"Starting extraction for {len(cities)} cities")
    weather_data = []
    max_workers = min(32, (multiprocessing.cpu_count() or 1) * 5)
    with ThreadPoolExecutor(max_workers) as executor:
        future_to_city = {executor.submit(fetch_with_retries, city): city for city in cities}
        success_count = 0
        failure_count = 0
        for future in as_completed(future_to_city):
            city = future_to_city[future]
            try:
                data = future.result()
                if data:
                    weather_data.append({"raw": data, "city": city})
                    success_count += 1
                else:
                    failure_count += 1
            except Exception as e:
                logging.error(f"Unexpected error for {city}: {e}")
                failure_count += 1

    logging.info(f"Extraction completed: {success_count} successful, {failure_count} failed")
    return weather_data
