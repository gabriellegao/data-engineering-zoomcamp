## ETL vs ELT
ETL or ELT is composed of three main stages - extract, transform, and load. 
### ETL
1. Slight more stable and compliant data analysis
2. Higher storage and compute costs

### ELT
1. Faster and more flexible data analysis
2. Lower cost and lower maintenance.

## Dimensisonal Modeling
### Elements of Dimensional Modeling
- Facts table  
- Dimension table
### Architecture of Dimensional Modeling
- Stage area  
- Processing area  
- Presentation area  

## DBT
dbt (data build tool) is designed to tranform raw data to ready-to-use data using SQL. dbt also provides functionalities, like deployment (version control and CI/CD), test and document, and development

### Materializations
1. Ephemeral  
   It's a temporary view and only exist during a single dbt run
2. View  
   View is a query-based table built on the top of the real table
3. Table  
   Table is physical representation of data that are created and stored in the database
4. Incremental  
   Incremental materialization decribe a process of incrementally loading new data to the existing table without dropping the whole table and recreate it again.

### Macro
Macro is a function acted like def function in python

There are two ways to define or call a macro function
```dbt
{{ macro_statement }} <-- double curly brackets
{% macro_statement %} <-- single curly brackets with a symbol
```

### Packages
Packages is dbt's libraries, including models and macros

### Variables
Variable defines value used across the project. It can be defined in two ways:
1. In `dbt_project.yml` file
2. On command line
```dbt
{{ var('variable_value') }}
```

### From Statment
There are two formats of from statement
1. `{{ source('staging','external_green_tripdata') }}`  
   This command is to call external tables and views that are not stored or controlled by dbt.  
   `staging` represents external database name and schema name and is defined in `schema.yaml`.
2. `{{ ref('stg_external_green_tripdata') }}`  
   This command is to call internal tables and view that are store or controlled by dbt.

### Test
Test is defined in `yaml` file for columns including:
1. Unique
   ```dbt
   tests:
     - unique:
        severity: warn
   ```
2. Not Null
   ```dbt
   tests:
     - not_null:
        severity: warn
   ```
3. Accepted Value
   ```dbt
   tests:
    - accepted_values:
        values: "{{ var('payment_type_values') }}"
        severity: warn
        quote: false
   ```
4. Relationships to other materializations
   ```dbt
   tests:
     - relationships:
       to: ref('taxi_zone_lookup')
       field: locationid
       severity: warn
   ```

### Documentation
生成HTML格式的文档  
```dbt
dbt docs generate
```

### Run Model
有两种方式可以运行models(`models`文件下的`sql`file)
1. `dbt run`  
   仅运行模型，不执行测试或者快照
2. `dbt build`  
   综合执行多个任务: `dbt run` + `dbt test` + `dbt snapshot` + `dbt seed`, 适合构建完整的dbt project

### Compile Model
将Jinjia模版解析成SQL文件
```dbt
dbt compile
```

### Install Packages
```dbt
dbt deps
```

### Create Dataset for dbt
Setting --> Credentials --> Development Credentials --> Type your new dataset name in dataset box  
The dbt will generate a new dataset in your GCP.

### Create `schema.yaml` in Staging Folder
```dbt
version: 2

sources:
  - name: staging
    database: <your_database_name>
    schema: <your_dataset_name>

    tables:
      - name: <table_name_1>
      - name: <table_name_2>
```

### Generate Schema
After installing `dbt-labs/codegen` in the `packages.yaml`, you can use the following command to generate the schema for you moedels. 
```dbt
{% set models_to_generate = codegen.get_models(directory='staging', prefix='stg') %}
{{ codegen.generate_model_yaml(
    model_names = models_to_generate
) }}
```
1. Click `Compile` button, the dbt will generate the schema for your models   
1. Copy the schema and paste to your `schema.yaml`

### Jobs
There two job types: normal job and CI job.  
*Jobs run on the top of main branch in repo. Don't forget to push the changes to main branch.*

1. Normal Job  
It can be manually triggered or be triggered by schedules. 

2. CI Job  
It's triggered by pull request in git repo

## DBT and BigQuery on Docker
### Setup
Create a folder to store all required files
```bash
mkdir <dir-name>
cd <dir-name>
```
### Dockerfile
[Dockerfile](docker/Dockerfile)
### Docker Compose YAML
[docker-compose.yaml](docker/docker-compose.yaml)
### Profiles YAML
[profile.yml](docker/.dbt/profiles.yml)
### Build Image and Containers
```bash
docker compose build 
docker compose run dbt-bq-dtc init
```
*Attention*  
*In `dbt_project.yml`, replace `profile: 'taxi_rides_ny'` with `profile: 'bq-dbt-workshop'` as we have a profile with the later name in our `profiles.yml`*
### Test Connection
```bash
docker compose run --workdir="//usr/app/dbt/taxi_rides_ny" dbt-bq-dtc debug
# Output: All checks passed!
```