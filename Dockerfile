# Dockerfile

FROM python:3.11-slim


ENV AIRFLOW_HOME=/opt/airflow

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ./dags /opt/airflow/dags
COPY ./src /opt/airflow/src
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/src"


CMD ["python", "src/main.py"]
