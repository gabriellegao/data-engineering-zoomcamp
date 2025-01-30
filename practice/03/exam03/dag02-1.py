from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

from push_xcom_value(**context):
    context['ti'].xcom_push(key='year', value=)


with DAG(
    dag_id = "main_dag",
    start_date = days_ago(1)
    schedule_interval='@once'
) as dags:
    for year in ['2019','2021','2022']:
        push_task = PythonOperator(
            task_id='push_task'
            python_callable=push_xcom_value
        )

# 用代码实现我不知道怎么写，但我的想法是，用xcom读取年份，然后子dag通过年份所以stroage里的对应数据，再用bigqueryinsertjoboperator()创建table
