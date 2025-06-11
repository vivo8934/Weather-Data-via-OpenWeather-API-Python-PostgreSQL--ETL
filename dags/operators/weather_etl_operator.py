from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from pipeline import run_pipeline
from config import CITIES

class WeatherETLOperator(BaseOperator):

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.log.info("Starting Weather ETL Pipeline")
        run_pipeline()
        self.log.info("Weather ETL Pipeline finished successfully")
