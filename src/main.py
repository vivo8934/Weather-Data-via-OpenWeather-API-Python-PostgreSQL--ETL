from extract import extract_weather_data
from transform import transform_weather_data
from load import load_to_postgres
from config import CITIES
import pandas as pd



if __name__ == "__main__":
    raw_weather = extract_weather_data(CITIES)
    df = transform_weather_data(raw_weather)
    #print("\n=== Weather Data for 10 SA Cities ===\n")
    print(df)
    load_to_postgres(df)