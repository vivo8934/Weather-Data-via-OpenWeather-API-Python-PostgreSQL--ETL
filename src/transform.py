import logging
import pandas as pd

def transform_weather_data(records):
    logging.info(f"Starting transformation on {len(records)} records")

    if not records:
        logging.warning("No records to transform")
        return pd.DataFrame()

    clean_data = []

    for item in records:
        raw = item.get("raw", {})
        location = raw.get("location", {})
        current = raw.get("current", {})

        try:
            city = location.get("name", item.get("city", "")).title().strip()
            region = location.get("region", "").title().strip()
            temp_c = current.get("temp_c")

            # Convert Fahrenheit if Celsius is missing
            if temp_c is None and current.get("temp_f") is not None:
                temp_c = round((current["temp_f"] - 32) * 5 / 9, 2)

            clean_data.append({
                "city": city,
                "region": region,
                "temperature_c": temp_c,
                "condition": current.get("condition", {}).get("text", "").strip(),
                "humidity": current.get("humidity"),
                "wind_kph": current.get("wind_kph"),
                "local_time": location.get("localtime"),
            })
        except Exception as e:
            logging.warning(f"Failed to process record for city: {item.get('city', 'unknown')}, error: {e}")

    df = pd.DataFrame(clean_data)
    before_drop = len(df)
    df = df.dropna(subset=["temperature_c", "local_time"])
    dropped = before_drop - len(df)

    logging.info(f"Dropped {dropped} records due to missing temperature or local time")
    logging.info(f"Transformation completed: {len(df)} records ready for loading")

    return df
