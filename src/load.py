import os
import logging
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

def load_to_postgres(df, table_name="weather_data"):
    conn, cur = None, None
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            database=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD")
        )
        cur = conn.cursor()

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

        rows = df.to_records(index=False)
        execute_batch(cur, f"""
            INSERT INTO {table_name} (city, region, temperature_c, condition, humidity, wind_kph, local_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, rows)

        conn.commit()
        logging.info(f"✅ Loaded {len(df)} records into '{table_name}'")

    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
