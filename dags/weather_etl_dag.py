from airflow import DAG
from datetime import datetime, timedelta
from operators.weather_etl_operator import WeatherETLOperator  # Import your operator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='weather_etl',
    default_args=default_args,
    description='ETL pipeline for weather data with custom operator',
    schedule_interval='@daily',
    start_date=datetime(2025,6,11),
    catchup=False,
    max_active_runs=1,
    tags=['weather', 'etl'],
) as dag:

    run_etl = WeatherETLOperator(
        task_id='run_weather_etl_pipeline',
    )
