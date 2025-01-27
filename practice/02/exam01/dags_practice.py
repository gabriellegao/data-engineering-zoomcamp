from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 1
}

dag = DAG(
    dag_id="simple_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False
)

download_task = BashOperator(
    task_id="download_data",
    bash_command="curl -sSL https://example.com/data.csv > /opt/airflow/data.csv",
    dag=dag
)

process_task = BashOperator(
    task_id="process_data",
    bash_command="python /opt/airflow/process_data.py",
    dag=dag
)

download_task >> process_task
'''
这道题我不太熟悉dag的各种书写格式，我比较习惯性使用
dag_name = DAG(xxx)
    with dag_name:
        xxxx
所以我不确定我这样的更改是不是正确的
以下是我比较熟悉的dag书写模式
'''
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 1
}

dag = DAG(
    dag_id="simple_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False
)
with dag:

    download_task = BashOperator(
        task_id="download_data",
        bash_command="curl -sSL https://example.com/data.csv > /opt/airflow/data.csv",
    )

    process_task = BashOperator(
        task_id="process_data",
        bash_command="python /opt/airflow/process_data.py"
        dag=dag
    )

    download_task >> process_task
