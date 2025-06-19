import time
from extract import extract_weather_data
from transform import transform_weather_data
from load import load_to_postgres
from config import CITIES

def run_pipeline(cities=CITIES, logger=None):
    logger = logger or __import__('logging').getLogger(__name__)

    logger.info("🔄 Extract step")
    raw = extract_weather_data(cities)
    logger.info(f"   → Fetched {len(raw)} records")

    logger.info("🔄 Transform step")
    df = transform_weather_data(raw)
    logger.info(f"   → Transformed {len(df)} records")

    logger.info("🔄 Load step")
    load_to_postgres(df)
    logger.info("   → Loaded {len(df)} records")
