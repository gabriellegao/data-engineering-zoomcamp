from airflow import DAG
from datetime import datetime

with DAG(
    dag_id = "practice-dag-01",
    start_date = datetime.now()
) as dag:
    taskB = TaskBOperator(
        task_id='taskB',
        xxx
        )

    taskA = TaskAOperator(
        task_id = 'taskA',
        XXX)

    taskB >> taskA