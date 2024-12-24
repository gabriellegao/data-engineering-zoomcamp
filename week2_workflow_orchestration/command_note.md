## Pre-requisite 
### Move and Rename Credential File
```bash mkdir ~/.google/credentials```
```bash mv <path_to_your_credential_json_file> ~/.google/credentials/google_credential.json```
--> 把之前terraform section创建的service account credential重新命名，添加到新建的folder中

### Upgrade your docker-compose version to v2.x+
```bash docker compose version```
```output: Docker Compose version v2.30.3-desktop.1```

### Set the memory for your Docker Engine to minimum 5GB (ideally 8GB)
在Docker Desktop可以直接更改设置, 调整至5-8GB
Setting -> Resources -> Advanced -> Memory Limit 

## Airflow Setup
### Creat a new folder named `airflow` in your current directory or your project directory
```bash mkdir ~/<path_to_your_project_directory>/airflow```

### Import official `docker-compose.yaml` file
```bash curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'```

### Create three new folders
```bash mkdir -p ./dags ./logs ./plugins```
--> 在airflow文件下，创建`dags`,`logs`,`plugs`

### Setup `AIRFLOW_UID`
```bash echo -e "AIRFLOW_UID=$(id -u)" > .env```

### Docker Build
1. 首先在airflow文档下面，创建`Dockerfile`
1. Repo里有设置好的版本，可以参考

### Docker Compose
1. 修改docker-compose.yaml中的设置
1. Repo里有设置好的版本，可以参考
1. 添加Line 47-49，删除自带的image设置（此段设置已经被添加到Dockerfile中）
1. 添加Line 76，`~/.google/credentials/:/.google/credentials:ro`
1. 修改Line 53 variable name, replace `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` with `AIRFLOW__CORE__SQL_ALCHEMY_CONN`
--> 修改后，后续代码可以正常运行，不修改的话，可能会报错，类似`airflow.exceptions.AirflowConfigException: error: cannot use sqlite with the CeleryExecutor`
1. 添加Line 63-64，更换成在terraform section时，创建的`project-id`和`gcp-bucket-id`
1. 添加Line66-70, Line 61-62
1. 更改Line58, change to `false`

## Execution
### Build Docker Image
```bash docker-compose build```
--> 读取`docker-compose.yaml`中指定的`Dockerfile`, 并创建镜像

### Initialize Airflow Settings
```bash docker-compose up airflow-init```
--> 初始化 Airflow 数据库和必要的配置
--> 启动docker-compose.yaml 中定义的 airflow-init 服务

### Kick Off All Services
```bash docker-compose up```
1. `airflow-webserver`: 提供 Web 界面，供用户访问和操作任务
1. `airflow-scheduler`: 调度任务，确保 DAG 按计划执行
1. `airflow-worker`: 执行任务（当使用 CeleryExecutor 时）
1. `redis`: 用作任务队列的消息代理
1. `postgres`: 用作 Airflow 的元数据库