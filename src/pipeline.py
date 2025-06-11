from extract import extract_weather_data
from transform import transform_weather_data
from load import load_to_postgres
from config import CITIES
import logging
import time

def run_pipeline():
    logging.info("Starting ETL pipeline for weather data")
    start = time.time()

    raw = extract_weather_data(CITIES)
    df = transform_weather_data(raw)
    load_to_postgres(df)

    logging.info(f"ETL pipeline completed in {round(time.time() - start, 2)}s")