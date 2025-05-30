import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from ingest_script import ingest_callable

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

URL_PREFIX = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
URL_TEMPLATE = URL_PREFIX + 'yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet'

OUTPUT_FILE_TEMPLATE_PARQUET = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.parquet'
OUTPUT_FILE_TEMPLATE_CSV = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y-%m\') }}'

PG_HOST = os.environ.get('PG_HOST')
PG_USER = os.environ.get('PG_USER')
PG_PASSWORD = os.environ.get('PG_PASSWORD')
PG_PORT = os.environ.get('PG_PORT')
PG_DATABASE =os.environ.get('PG_DATABASE')

local_workflow  = DAG(
    dag_id = 'LocalIngestionDag',
    schedule_interval="0 6 2 * *",
    start_date = datetime(2024,8,1),
    catchup=False
)

with local_workflow:
    curl_task = BashOperator(
        task_id='curl',
        bash_command = f'curl -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE_PARQUET}'
        
    )

    ingest_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest_callable,
        op_kwargs=dict(
            user = PG_USER, 
            password = PG_PASSWORD, 
            host = PG_HOST, 
            port = PG_PORT, 
            db = PG_DATABASE, 
            table_name = TABLE_NAME_TEMPLATE, 
            parquet_file=OUTPUT_FILE_TEMPLATE_PARQUET,
            csv_file=OUTPUT_FILE_TEMPLATE_CSV
        )
    )
   

    curl_task >> ingest_task