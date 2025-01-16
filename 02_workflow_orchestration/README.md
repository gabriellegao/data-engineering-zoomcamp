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
读取`docker-compose.yaml`中指定的`Dockerfile`, 并创建镜像
```bash 
docker-compose build
```

### Initialize Airflow Settings
初始化 Airflow 数据库和必要的配置  
启动docker-compose.yaml 中定义的 airflow-init 服务  
```bash 
docker-compose up airflow-init
```

### Kick Off All Services
```bash 
docker-compose up
```
1. `airflow-webserver`: 提供 Web 界面，供用户访问和操作任务
1. `airflow-scheduler`: 调度任务，确保 DAG 按计划执行
1. `airflow-worker`: 执行任务（当使用 CeleryExecutor 时）
1. `redis`: 用作任务队列的消息代理
1. `postgres`: 用作 Airflow 的元数据库

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