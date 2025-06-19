# /opt/airflow/dags/weather_etl_dag.py

import sys
import os

# 1) Ensure /opt/airflow/src is in the import path so we can import our modules
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from airflow import DAG
from airflow.utils.dates import days_ago
from operators.weather_etl_operator import WeatherETLOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="weather_etl",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    tags=["weather", "etl"],
) as dag:
    

    run_weather = WeatherETLOperator(
        task_id="run_weather_etl_pipeline",
        # cities=None will use defaults from config.py in src/
    )
