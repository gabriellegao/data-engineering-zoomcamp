# 选择题
1. D
2. A
3. A
4. B
5. B (这道题我是在网上查的，我想知道有没有什么方法能够判定哪些是linux env依赖，哪些是python依赖)

# 填空题
1. dag task
2. 确保service之间的运行顺序，比如airflow-init要开始，必须先得安装好redies and postgres
3. task instance (这道题不确定)
4. 在创建image时，更新并安装这个library，并且auto-approve (-y的代表的指令 我不确定)
5. CeleryExecutor （不确定，我没找到cfg file，我是在yaml里面找到的这个）

# 代码题
1.  
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 1
}

dag = DAG("xcom_example", default_args=default_args, schedule_interval="@daily")

def push_xcom(**kwargs):
    value = "Hello, Airflow!"
    kwargs['ti'].xcom_push(key="message", value=value)

def pull_xcom(**kwargs):
    value = kwargs['ti'].xcom_pull(task_ids='push_task', key='message')
    print(f"Received XCom Value: {value}")

task_1 = PythonOperator(
    task_id="task_1",
    python_callable=push_xcom,
    provide_context=True,
    dag=dag
)

task_2 = PythonOperator(
    task_id="task_2",
    python_callable=pull_xcom,
    provide_context=True,
    dag=dag
)

task_1 >> task_2

```
2.  
- 可能是前面的任务一直没跑完，那就得看下前面任务为什么卡住了
- 可能是前面任务报错，接下来的任务有依赖关系，所以卡住，那就把前面任务的bug给处理掉
- 可能一直在retry，但retries的次数设置太高，比如几十次，就导致任务一直queue

3.  
- 第一题：可以保证先启动redis，在启动postgres
- 第二题：不知道
- 第三题：定义host name
- redis and postgres下面可以加个condition: service_healthy