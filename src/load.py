import os
import logging
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

load_dotenv()

def load_to_postgres(df: pd.DataFrame, table_name="weather_data"):
    if df.empty:
        logging.warning("DataFrame is empty. Nothing to load.")
        return

    # Database connection info
    db_config = {
        "host": os.getenv("PG_HOST", "postgres_airflow"),
        "port": os.getenv("PG_PORT", 5432),
        "dbname": os.getenv("PG_DB", "weather_db"),
        "user": os.getenv("PG_USER", "weather_user"),
        "password": os.getenv("PG_PASSWORD", "weather_pass")
    }

    conn = None
    try:
        logging.info(
            "Connecting to Postgres with config: %s",
            {k: ("***" if k == "password" else v) for k, v in db_config.items()}
        )
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Ensure table exists
        logging.info(f"Ensuring table '{table_name}' exists...")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                city TEXT,
                region TEXT,
                temperature_c REAL,
                condition TEXT,
                humidity INTEGER,
                wind_kph REAL,
                local_time TIMESTAMP
            );
        """)
        conn.commit()

        # Build a list of native-Python tuples from DataFrame rows
        rows = []
        for rec in df.itertuples(index=False, name=None):
            city, region, temp_c, condition, humidity, wind_kph, local_time = rec
            rows.append((
                city,
                region,
                float(temp_c) if temp_c is not None else None,
                condition,
                int(humidity) if humidity is not None else None,
                float(wind_kph) if wind_kph is not None else None,
                local_time,  # pandas.Timestamp adapts fine to psycopg2
            ))

        logging.info(f"Inserting {len(rows)} records into '{table_name}'...")
        if not rows:
            logging.warning("No rows to insert after conversion.")
            return

        # Optional: log a sample
        logging.debug(f"Sample row: {rows[0]}")

        # Batch insert
        execute_batch(
            cur,
            f"""
            INSERT INTO {table_name}
              (city, region, temperature_c, condition, humidity, wind_kph, local_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            rows
        )
        conn.commit()
        logging.info(f"Successfully loaded {len(rows)} records into '{table_name}'")

    except Exception as e:
        logging.error("Error loading data: %s", e, exc_info=True)
        if conn:
            conn.rollback()
        raise

    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")
