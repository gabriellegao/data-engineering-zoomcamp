import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago

# Our airflow operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Helps us to interact with GCP Storage
from google.cloud import storage

# To allow us to interact with BigQuery
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

# Helps to convert our data to parquet format
import pyarrow.csv as pv
import pyarrow.parquet as pq

from datetime import datetime

# 假定我在docker-compose.yaml里面已经设定好这些variables
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/data/")
FILE_URL = "https://example.com/data.csv"
OUTPUT_CSV_PATH=AIRFLOW_HOME + "/data.csv"
OUTPUT_PARQUET_PATH = AIRFLOW_HOME + "/data.parquet"

def csv_to_parquet(src_file):
    if not src_file.endwith('csv'):
        logging.error("Only accept parquet files")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))

def upload_to_gcs(bucket, object_name, local_file):

    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

with DAG(
    dag_id="upload_parquet_to_gcs_dag",
    schedule_interval="@daily",
    start_date=datetime().now()
) as dags:
    
    dowload_data_task = BashOperator(
        take_id="download_data_task",
        bash_command = f'curl -sSL {FILE_URL} > {OUTPUT_CSV_PATH}'
    )

    transform_file_task = PythonOperator(
        task_id="transform_file_task",
        python_callable=csv_to_parquet,
        op_kwargs={
            "src_file": {OUTPUT_PARQUET_PATH}
        }
    )

    local_to_gcs_taks = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket":{BUCKET},
            "object_name":"my-bucket/data/",
            "local_file": {OUTPUT_PARQUET_PATH}
        }
    )

    dowload_data_task >> transform_file_task >> local_to_gcs_taks