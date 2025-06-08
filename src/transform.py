import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

def transform_weather_data(records):
    logging.info(f"Starting transformation on {len(records)} records")
    clean_data = []

    for item in records:
        raw = item.get("raw", {})
        location = raw.get("location", {})
        current = raw.get("current", {})

        try:
            city = location.get("name", item["city"]).title().strip()
            region = location.get("region", "").title().strip()
            temp_c = current.get("temp_c")
            if temp_c is None and current.get("temp_f") is not None:
                temp_c = round((current["temp_f"] - 32) * 5 / 9, 2)

            clean_data.append({
                "city": city,
                "region": region,
                "temperature_c": temp_c,
                "condition": current.get("condition", {}).get("text", "").strip(),
                "humidity": current.get("humidity"),
                "wind_kph": current.get("wind_kph"),
                "local_time": location.get("localtime")
            })
        except Exception as e:
            logging.warning(f"Failed to process record for city: {item.get('city')}, error: {e}")

    df = pd.DataFrame(clean_data)
    before_drop = len(df)
    df = df.dropna(subset=["temperature_c", "local_time"])
    dropped = before_drop - len(df)
    logging.info(f"Dropped {dropped} records due to missing temperature or local time")

    return df
