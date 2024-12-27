import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago

# To allow us to interact with BigQuery
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator

# Take environmental variables into local variables. These were set in the docker-compose setup.
# These two variables load into docker environment as environment variables when running the docker-compose.yaml
# os.environ.get searchs for these two variables in docker environment 
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "trips_data_all")

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    gcs_2_gcs_task=GCSToGCSOperator(
        task_id='gcs_2_gcs_task',
        source_bucket = BUCKET,
        source_object='raw/yellow_tripdata/*.parquet',
        destination_bucket=BUCKET,
        destination_object ='yellow/*' ,
        move_object=True

    )

    gcs_2_bq_ext_task = BigQueryCreateExternalTableOperator(
        task_id="gcs_2_bq_ext_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_yellow_tripdata_week3",
            },
            "externalDataConfiguration": {
                "autodect": True,
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/yellow/*"],
            },
        },
    )

    CREATE_PART_TBL_QUERY = f"CREATE OR REPLACE TABLE {PROJECT_ID}.{BIGQUERY_DATASET}.external_yellow_tripdata_week3\
    PARTITION BY \
    DATE(tpep_pickup_datetime) AS \
    SELECT * FROM {BIGQUERY_DATASET}.external_yellow_tripdata__partitioned_week3"

    bq_ext_2_part_task = BigQueryInsertJobOperator(
        task_id = "bq_ext_2_part_task",
        configuration={
            "query": {
                    "query": CREATE_PART_TBL_QUERY,
                    "useLegacySql": False,
                }
            }

    )

    gcs_2_gcs_task >> gcs_2_bq_ext_task >> bq_ext_2_part_task