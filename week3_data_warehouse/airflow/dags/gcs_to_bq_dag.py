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
# with DAG(
#     dag_id="data_ingestion_gcs_dag",
#     schedule_interval="@daily",
#     default_args=default_args,
#     catchup=False,
#     max_active_runs=1,
#     tags=['dtc-de'],
# ) as dag:

def gcs_bq_tbl_dag(
        dag,
        color,
        pickup_datetime

):
    with dag:

        # gcs_2_gcs_task=GCSToGCSOperator(
        #     task_id='gcs_2_gcs_task',
        #     source_bucket = BUCKET,
        #     source_object=source_object,
        #     destination_bucket=BUCKET,
        #     destination_object =destination_object ,
        #     move_object=move_object

        # )

        gcs_2_bq_ext_task = BigQueryCreateExternalTableOperator(
            task_id="gcs_2_bq_ext_task",
            table_resource={
                "tableReference": {
                    "projectId": PROJECT_ID,
                    "datasetId": BIGQUERY_DATASET,
                    "tableId": f"external_{color}_tripdata",
                },
                "externalDataConfiguration": {
                    "autodect": True,
                    "sourceFormat": "PARQUET",
                    "sourceUris": [f"gs://{BUCKET}/{color}/{color}_tripdata_2019-01.parquet"],
                }
    #             "schema": {
    #                 "fields": [
    #                     {"name": "VendorID", "type": "INTEGER"},
    #                     {"name": "tpep_pickup_datetime", "type": "TIMESTAMP"},
    #                     {"name": "tpep_dropoff_datetime", "type": "TIMESTAMP"},
    #                     {"name": "passenger_count", "type": "FLOAT"},
    #                     {"name": "trip_distance", "type": "FLOAT"},
    #                     {"name": "RatecodeID", "type": "FLOAT"},
    #                     {"name": "store_and_fwd_flag", "type": "STRING"},
    #                     {"name": "PULocationID", "type": "INTEGER"},
    #                     {"name": "DOLocationID", "type": "INTEGER"},
    #                     {"name": "payment_type", "type": "INTEGER"},
    #                     {"name": "fare_amount", "type": "FLOAT"},
    #                     {"name": "extra", "type": "FLOAT"},
    #                     {"name": "mta_tax", "type": "FLOAT"},
    #                     {"name": "tip_amount", "type": "FLOAT"},
    #                     {"name": "tolls_amount", "type": "FLOAT"},
    #                     {"name": "improvement_surcharge", "type": "FLOAT"},
    #                     {"name": "total_amount", "type": "FLOAT"},
    #                     {"name": "congestion_surcharge", "type": "FLOAT"},
    #                     {"name": "airport_fee", "type": "INTEGER"}
    # ]
# }
            },
        )

        CREATE_PART_TBL_QUERY = f"CREATE OR REPLACE TABLE de_zoomcamp_dataset.external_{color}_tripdata_partitioned\
        PARTITION BY \
        DATE({pickup_datetime}) AS \
        SELECT * FROM de_zoomcamp_dataset.external_{color}_tripdata"

        bq_ext_2_part_task = BigQueryInsertJobOperator(
            task_id = "bq_ext_2_part_task",
            configuration={
                "query": {
                        "query": CREATE_PART_TBL_QUERY,
                        "useLegacySql": False,
                    }
                }

        )

    # gcs_2_gcs_task 
    gcs_2_bq_ext_task >> bq_ext_2_part_task

yellow_taxi_data_dag = DAG(
    dag_id='yellow_taxi_data_tranform',
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],    
)

gcs_bq_tbl_dag(
    dag = yellow_taxi_data_dag,
    color='yellow',
    pickup_datetime='tpep_pickup_datetime'

)

green_taxi_data_dag = DAG(
    dag_id='green_taxi_data_transform',
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],    
)

gcs_bq_tbl_dag(
    dag=green_taxi_data_dag,
    color='green',
    pickup_datetime='lpep_pickup_datetime'

)

