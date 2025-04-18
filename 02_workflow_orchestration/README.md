## Pre-requisite 
### Move and Rename Credential File
把之前terraform section创建的service account credential重新命名，添加到新建的folder中  
```bash
bash mkdir ~/.google/credentials
mv <path_to_your_credential_json_file> ~/.google/credentials/google_credential.json
```


### Upgrade your docker-compose version to v2.x+
```bash 
docker compose version
# Output: Docker Compose version v2.30.3-desktop.1
```


### Set the memory for your Docker Engine to minimum 5GB (ideally 8GB)
在Docker Desktop可以直接更改设置, 调整至5-8GB
Setting -> Resources -> Advanced -> Memory Limit 

## Airflow Setup
### Creat a new folder named `airflow` in your current directory or your project directory
```bash 
mkdir ~/<path_to_your_project_directory>/airflow
```

### Import official `docker-compose.yaml` file
```bash 
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```

### Create three new folders
在airflow文件下，创建`dags`,`logs`,`plugs`
```bash 
mkdir -p ./dags ./logs ./plugins
```


### Setup `AIRFLOW_UID`
```bash 
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

### Docker Build
1. 首先在airflow文档下面，创建`Dockerfile`
1. Repo里有设置好的版本，可以参考

### Docker Compose Revise
1. 修改docker-compose.yaml中的设置
1. Repo里有设置好的版本，可以参考
1. 添加Line 47-49，删除自带的image设置（此段设置已经被添加到Dockerfile中）
1. 添加Line 76，`~/.google/credentials/:/.google/credentials:ro`
1. 修改Line 53 variable name, replace `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` with `AIRFLOW__CORE__SQL_ALCHEMY_CONN`
--> 修改后，后续代码可以正常运行，不修改的话，可能会报错，类似`airflow.exceptions.AirflowConfigException: error: cannot use sqlite with the CeleryExecutor`
1. 添加Line 63-64，更换成在terraform section时，创建的`project-id`和`gcp-bucket-id`
1. 添加Line66-70, Line 61-62
1. 更改Line58, change to `false`

### Docker Compose Concepts
- `x-`开头的字段为`YAML`扩展字段, 不会被解析成services
- 需要启动的services, 须放在`services:`字段后
- `&`为锚点, 覆盖的字段从锚点开始, 直到第一个缩进前结束。锚点覆盖的内容可以被后续的services用`<<: *`直接调用.
- 虽然几个service都调用了锚点下的`image build`, 但是如果Docker发现image已经被构建过, 则不会重复构建, 而是直接拉取此image
## Execution
### Build Docker Image
读取`docker-compose.yaml`中指定的`Dockerfile`, 并创建镜像
```bash 
docker-compose build
```

### Initialize Airflow Settings
初始化 Airflow 数据库和必要的配置, 并根据 `depends_on` 配置，确保 `redis` 和 `postgres` 服务先运行,且启动 `docker-compose.yaml` 中定义的 `airflow-init` 服务。  
```bash 
docker-compose up airflow-init
```

### Kick Off All Services
启动 `docker-compose.yaml` 中定义的所有服务（除了 `airflow-init`, 因为它已经完成了任务并退出）
```bash 
docker-compose up
```
1. `airflow-webserver`: 提供 Web 界面，供用户访问和操作任务
1. `airflow-scheduler`: 调度任务，确保 DAG 按计划执行
1. `airflow-worker`: 执行任务（当使用 CeleryExecutor 时）
1. `redis`: 用作任务队列的消息代理
1. `postgres`: 用作 Airflow 的元数据库

### Service Diagram
docker compose build  
$\quad$  ↓  
docker compose up airflow-init  
  ├── 启动 redis  
  ├── 启动 postgres  
  └── 运行 airflow-init 完成初始化  
$\quad$  ↓  
docker compose up  
  ├── 启动 airflow-webserver  
  ├── 启动 airflow-scheduler  
  ├── 启动 airflow-worker  
  └── 启动 flower  


***如果环境变量发生改变，需按照以上三步重新启动docker***

## DGAs
### Definition
在 Apache Airflow 中，DAGs 是 Directed Acyclic Graphs（有向无环图） 的简称。它是 Airflow 的核心概念，用于定义任务的执行顺序和依赖关系。简单来说，DAG 是 Airflow 的工作流框架，用于组织和调度一组任务。

### Architecture
1. DAGs定义：用于设置工作流的调度属性，比如名字、开始时间、运行间隔等。
1. Tasks: 实际的操作，比如运行脚本、移动文件、调用 API 等。
1. 任务执行顺序：任务之间通过依赖关系连接，定义了执行顺序。

## Additional Notes
### Download data from url
```bash
curl -sSL <url> > <path_to_the_file>
```
从网页上下载文件，`L`意思是，如果link跳转到其他页面，会自动跟随

### Setup environment variable
1. Terminal
```bash
export variable_name = variable_value
```
1. .env
```python
variable_name = variable_value
```

1. docker-compose.yaml
```bash
environment:
    varibale_name = variable_value
```

### Schedule Expression Generator
[Crontab Guru](https://crontab.guru/)

### Airlfow Xcom
`Xcom`是一次性读取所有数据, 而不是逐一读取
```python
from airflow.operators.python import PythonOperator

def push_xcom_value(**kwargs):
    kwargs['ti'].xcom_push(key='my_key', value='my_value')

def pull_xcom_value(**kwargs):
    value = kwargs['ti'].xcom_pull(task_id='push_task', key='my_key')
    print(f"Received XCom Value: {value}")

push_task = PythonOperator(
    task_id='push_task',
    python_callable=push_xcom_value,
    provide_context=True
)

pull_task = PythonOperator(
    task_id='pull_task',
    python_callable=pull_xcom_value,
    provide_context=True
)

push_task >> pull_task
```
### Airflow Kwargs
- `kwargs['execution_date']`: DAG 任务的逻辑执行时间
- `kwargs['ti']`: 任务实例
  - `ti.xcom_push(key, value)`: 将数据存入 XCom
  - `ti.xcom_pull(task_ids, key)`: 从 XCom 取出数据
  - `ti.execution_date`: 任务的逻辑执行时间
  - `ti.start_date`: 任务实际开始执行的时间
  - `ti.end_date`: 任务执行完成的时间
- `kwargs['conf']`: 读取airflow全局配置
  
### Check Airflow Task Status
```bash
docker-compose ps            # 检查所有服务
docker-compose logs scheduler  # 查看 Scheduler 日志
airflow dags list            # 列出所有 DAG
airflow tasks list <dag_id>   # 查看 DAG 里的任务
airflow tasks test <dag_id> <task_id> <execution_date>  # 运行单个任务
```

### Airflow Jinja
Jinjia模版只能在`PythonOperator`和`BashOperator`中使用:
- `PythonOperator`: 在`templates_dict`中定义, 在`op_kwargs`中调用
```python
ingest_task = PythonOperator(
    task_id="ingest",
    python_callable=ingest_callable,
    templates_dict={
        "table_name": "yellow_taxi_{{ execution_date.strftime('%Y-%m') }}"
    },
    provide_context=True,
    op_kwargs={
        "table_name": "{{ templates_dict['table_name'] }}"
    },
)
```
- BashOperator: 在params中定义, 在bash_command中调用
```python
curl_task = BashOperator(
    task_id="curl",
    bash_command='curl -sSL {{ params.url }} > {{ params.output_file }}',
    params={
        "url": URL_TEMPLATE,
        "output_file": OUTPUT_FILE_TEMPLATE_PARQUET
    }
)
```