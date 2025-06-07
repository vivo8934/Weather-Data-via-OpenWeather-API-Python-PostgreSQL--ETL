from extract import extract_weather_data
from config import CITIES
import pandas as pd

raw_weather = extract_weather_data(CITIES)

if __name__ == "__main__":
    df = pd.DataFrame(raw_weather)
    print("\n=== Weather Data for 10 SA Cities ===\n")
    print(df)