# operators/weather_etl_operator.py

import sys, os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "src")
    )
)

from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from pipeline import run_pipeline
from config import CITIES

class WeatherETLOperator(BaseOperator):
    def __init__(self, cities=None, **kwargs):
        super().__init__(**kwargs)
        self.cities = cities or CITIES

    def execute(self, context: Context):
        self.log.info("📡 Starting Weather ETL")
        run_pipeline(cities=self.cities, logger=self.log)
        self.log.info("✅ Weather ETL complete")
