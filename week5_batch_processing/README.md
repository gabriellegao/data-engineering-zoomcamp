## Data Processing
Data Processing分两种类型
1. Batch processing
2. Stream processing

## Install Java
### Download Package
```bash
mkdir spark/
cd spark/
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
```
### Unpack Package
```bash
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz
```

### Remove Installer
```bash
rm openjdk-11.0.2_linux-x64_bin.tar.gz
```

### Define `JAVA_HOME` and Add It to `PATH`
- The variable name `JAVA_HOME` is immutable (Don't change it)
- Mapping the original path to `PATH` allows us to call this command or its executable file across all directories. 
```bash
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"
```

## Install Spark
### Download Package
```bash
wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
```
*In the same folder as `java`*

### Unpack Package
```bash
tar xzfv spark-3.3.2-bin-hadoop3.tgz
```

### Remove Installer
```bash
rm spark-3.3.2-bin-hadoop3.tgz
```
### Remove Installer
```bash
rm spark-3.3.2-bin-hadoop3.tgz
```

### Define `SPARK_HOME` and Add It to `PATH`
```bash
export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```
## Config PySpark
### Define `PYTHONPATH` AND Add It to `PATH`
```bash
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```
*Run this two commands before start Jupyter Notebook*

## Download Massive Data from URL
- Use `.sh` file to download ny taxi data for yellow and green from 2020 to 2021
- Link: [download_data.sh](download_data.sh)
```bash
./download_data.sh <param1> <param2>
```

## PySpark Script
### Port
Add port `8888` to port pannel in vscode. This port links to Jupyter Notebook
Add port `4040` to port pannel in vscode. This port links to Spark Job webppage.

### Download Taxi Zone Data
Download this file in Jupyter Notebook
```bash
!wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

### Load Data in Spark
```python
import pyspark
from pyspark.sql import SparkSession

# Build a Local Spark Cluster(inside notebook)
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df = spark.read \
    .option("header", "true") \
    .csv('taxi_zone_lookup.csv')

df.show()
```

### Write Data in Parquet Format
```python
df.write.parquet('zones')
```

### Schema Commands
- Define Schema
```python
# Import schema required packages
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType
# Define Schema
schema = StructType([
    StructField('hvfhs_license_num', StringType(), True), 
    StructField('dispatching_base_num', StringType(), True), 
    StructField('pickup_datetime', TimestampType(), True), 
    StructField('dropoff_datetime', TimestampType(), True), 
    StructField('PULocationID', IntegerType(), True), 
    StructField('DOLocationID', IntegerType(), True)])
```
- Print Schema
```python
df.schema
df.printSchema()
```
### Output Commands
```pthon
.show()
.take(num_records)
.head(num_records)
.write
```

### Partition
```python
df.repartition(num_layers)
```

### UDF
UDF is abbreviation of User Defined Function
```python
# Import packages
from pyspark.sql import functions as F
# Define a udf function
def crazy_stuff(base_num):
    num = int(base_num[1:])
    if num % 7 == 0:
        return f's/{num:03x}'#0 means filling 0 if length<3
    elif num % 3 == 0:
        return f'a/{num:03x}'#3 means the length of number
    else:
        return f'e/{num:03x}'#x means Hexadecimal 16
# Save function as udf and define its output type
crazy_stuff_udf = F.udf(crazy_stuff, returnType = StringType())
# Call functin
df.withColumn('base_id', crazy_stuff_udf(df.dispatching_base_num))
```

### Repartition
Partition table into multi files. The number of output files are the same as the `num_layers`.
```python
df.repartition(num_layers).write
```

## Spark Internal
### Spark Cluster
We need to split the data file to multiple partition.  
The Driver Node assigns each partition to each Worker Node, and Worker Node process the job.  
After completing the job, the Worker Node will be assigned next job and process it again until all the jobs are finished.

### Spark GroupBy
Stage 1
   - Process data in each partition with filter and groupby. 
   - Output the result for each partition

Intermediate Stage
   - Reshuffling, moving outputs from each partition to next new partition.
   - In each new partition, the records are sorted and have the same groupby
   - The algorithm of Reshuffling is called External Merge Sort
  
Stage 2 
   - Place the same groupby into one block (partition).
   - Complete the rest of jobs (e.g. aggregation) 
### Spark Join
Stage 1
    - Process data and generate keys (join keys) for each record

Intermediate Stage
    - Reshuffling, place the same keys into new partitions
  
Stage 2
    - Combine record with the same key into one row

### Spark Broadcast
- Broadcast happens when joining a small dataframe.  
- Each Worker Nodes copy the entire small dataframe and the join happens in memory.

## Resilient Distributed Datasets (RDD): Map and Reduce
### Definition of RDD
- Resilient: Fault-tolerant and capable of recomputing lost data from the lineage (a history of transformations used to build the dataset).
- Distributed: The data is divided across multiple nodes in a cluster, enabling parallel processing.
- Dataset: A collection of records, where each record can be an object, such as a row in a dataset.
### Where in DataFrame vs. Filter in RDD

- Define a filter function `filter_func`
```python
def filter_func(row):
    return row.column >= benchmark
```
- Call `filter_func` in RDD filter  
- `filter_func` read each row in `rdd` and return results  
```python
rdd.filter(filter_func)
```
***Attention***
```python
# Wrong format 
rdd.filter(filter_func(row))
```
This expression process values representing by `row` using `filter_func` instead of each row in `rdd`  
```python
# Output for `rdd.filter(filter_func(row))`
rdd.filter(True)
```

### GroupBy in DataFrame vs. Map and ReduceByKey in RDD
- Prepare keys and values
- Composite key = (`hour`, `zone`)
- Composite value = (`amount`, `count`)
```python
def key_value_func(row):
    hour = row.lpep_pickup_datetime\
                .replace(minute=0, second=0, microsecond=0)
    zone = row.PULocationID
    key = (hour, zone)
    
    amount = row.total_amount
    count = 1
    value = (amount, count)
    
    return (key,value)
```
- Calculate Sum
- Sum up values (composite value) with the same key (composite key)
```python
def calculate_sum(left_value, right_value):
    left_amount, left_count = left_value
    right_amount, right_count = right_value
    
    output_amount = left_amount + right_amount
    output_count = left_count + right_count
    
    return (output_amount, output_count)
```
- Call functions: `key_value_func` and `calculate_sum`
```python
rdd\
    .map(key_value_func)\
    .reduceByKey(calculate_sum)
# Output:[((key1,key2), (value1, value2))((...),(...))]
```
### RDD to DataFrame: Map and ToDF
- Define a `unwrap` function to format each row 
```python
def unwrap(row):
    return (row[0][0], row[0][1], row[1][0], row[1][1])
```
- Call `unwrap` function
```python
rdd.map(unwrap)\
    .toDF()
# Output : [(key1, key2, value1, value2),(...)]
```

### Naming Columns
- Define a namedtuple function `revenuerow` and assign column names
```python
from collections import namedtuple
revenuerow = namedtuple('revenuerow', ['hour','zone','revenue','count'])
```
- Call `revenuerow` functions and assign value to each column
```python
def unwrap(row):
    return revenuerow(
        hour = row[0][0], 
        zone = row[0][1], 
        revenue = row[1][0], 
        count = row[1][1])
```
- Return a dataframe with column names
```python        
rdd.map(unwrap)\
    .toDF()\
    .show()
```
## RDD: MapPartition
### Definition of MapPartition
MapPartition process RDD by partition. Each partition is a iterator
```python
rdd.mapPartition(func)
```
### Map vs. MapPartition
- Map process RDD by row
- MapPartition process RDD by partition

### RDD to Pandas DataFrame
```python
import pandas as pd
columns = [....]
rows = rdd.take(5)
df = pd.DataFrame(rows, columns = columns)
```

### Pandas DataFrame to RDD
- Yield
  - Generator function, similar as iterator
  - Yield here add each row into a iterator  
- Itertuples
  - Used only for Panda DataFrame, iterating each row
```python
def func(df):
    for row in df.itertuples():
        yield row
```
```python
# Example Code
def yield_iter():
    yield 1
    yield 2
    yield 3
gen = yield_iter
next(gen)
list(gen)
```

### RDD to Spark DataFrame
```python
rdd.toDF(schema).show()
```

### Iterator
```python
list = [1,2,3]
list_iter = iter(list)
next(list_inter)
# Output:
# 1
# 2
# 3
list(list_iter)
# Output: [1,2,3]
```
## Connect Spark to GCS (Local Built-in Spark Cluster)
### Upload Data to GCS
```bash
gsutil -m cp -r pq/ gs://nifty-structure-252803-terra-bucket/pq
```
- `cp`: cppy  
- `-r`: recursive  
- `-m`: use all cpus  

### Download Google Cloud Storage Connector for Hadoop
```bash
mkdir lib/
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar gcs-connector-hadoop3-2.2.5.jar
```

### Connect Spark to GCS (Local Built-in Spark Cluster)
```python
# Import Packages
import pyspark
from pyspark.sql import SparkSession
from datetime import datetime
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

# Credential location needs to be full path, "~" is not accepted
credentials_location = '/home/gabrielle/.google/credentials/google_credentials.json'

# Setup Spark Configuration and GSC Authentication
conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "./lib/gcs-connector-hadoop3-2.2.5.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)

# Build Spark Context
sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

# Build Spark Session
spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()

# Call Spark and Read Data from GCS
df = spark.read.parquet()

# Stop Spark Context
SparkContext._active_spark_context.stop()
```

## Create a Local Custom Spark Cluster
### Install Spark Standalone
- Location `sbin` folder in `~/home/gabrielle/spark/spark-3.3.2-bin-hadoop3`
```bash
./sbin/start-master.sh
```

### Ports
- `8080`: Monitor Spark Jobs
- `7077`: Master Port

### Initialize Worker/Slave Shell
```bash
# Old version: start-slaves.sh, New version: start-worker.sh
# Find URL in localhost:8080
./sbin/start-worker.sh spark://de-zoomcamp.us-central1-c.c.nifty-structure-252803.internal:7077
```
### Convert Jupyter Notebook to Python Script
```bash
jupyter nbconvert --to=script <notebook_name>
```

### Run Python Script
```bash
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
python <notebook_name>
```

### Run Python Script with Args
- Master URL(Master Node and Master Port) was set inside of py script
- Master URL: `.master("spark://de-zoomcamp.us-central1-c.c.nifty-structure-252803.internal:7077")`
```bash
python 08_local_spark_cluster.py \
    --input_green=data/pq/green/2020/*/ \
    --input_yellow=data/pq/yellow/2020/*/ \
    --output=data/report/report-2020
```

### Run Python Script with Args and Master URL
- Submit Spark Jobs to Spark Cluster
- Link: [08_local_spark.py](08_local_spark.py)
```bash
URL="spark://de-zoomcamp.us-central1-c.c.nifty-structure-252803.internal:7077"
spark-submit \
    --master="${URL}" \
    08_local_spark_cluster.py \
      --input_green=data/pq/green/2021/*/ \
      --input_yellow=data/pq/yellow/2021/*/ \
      --output=data/report-2021
```

## Create a Dataproc Cluster
### Upload Python Script to GSC Bucket
```bash
gsutil cp 08_local_spark_cluster.py gs://nifty-structure-252803-terra-bucket/code/08_local_spark_cluster.py
```
### Submit Job in Console
- Head to cluster page and click `Submit Job`
- Copy the file path into `Main Python File` box
- Add arguments to `Arguments` box
```bash
--input_green=gs://nifty-structure-252803-terra-bucket/pq/green/2021/*/ 
--input_yellow=gs://nifty-structure-252803-terra-bucket/pq/yellow/2021/*/ 
--output=gs://nifty-structure-252803-terra-bucket/report-2021
```

### Submit Job in `gcloud`
- Add `Dataproc Admin` access to service account
```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=us-central1 \
    gs://nifty-structure-252803-terra-bucket/code/08_local_spark_cluster.py \
    -- \
        --input_green=gs://nifty-structure-252803-terra-bucket/pq/green/2020/*/ \
        --input_yellow=gs://nifty-structure-252803-terra-bucket/pq/yellow/2020/*/ \
        --output=gs://nifty-structure-252803-terra-bucket/report-2020
```

## Connect Spark to BigQuery (Dataproc Cluster)
### Update Parquet Write Command
- Link: [09_spark_dataproc_cluster_bigquery](09_spark_dataproc_cluster_bigquery.py)
```python 
df_result.write.format('bigquery')\
    .option("table", output) \
    .save()
```
### Upload Python Script to GCS Bucket
```bash
gsutil cp 09_spark_dataproc_cluster_bigquery.py gs://nifty-structure-252803-terra-bucket/code/09_spark_dataproc_cluster_bigquery.py
```
### Submit Job in `gcloud` 
```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=us-central1 \
    # For my VM, it doesn't like jars config, so I commented it out
    # --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \ 
    gs://nifty-structure-252803-terra-bucket/code/09_spark_dataproc_cluster_bigquery.py \
    -- \
        --input_green=gs://nifty-structure-252803-terra-bucket/pq/green/2020/*/ \
        --input_yellow=gs://nifty-structure-252803-terra-bucket/pq/yellow/2020/*/ \
        --output=de_zoomcamp_dataset.report-2020
```
## Additional Notes
List all the file including hidden one
```bash
ls -a
```
List is extended list, listing file's size, access, modified date, etc.
```bash
ls -lh
```

Return the row count of file
```bash
wc -l <file_name>
```

Save the firt 1001 rows to `head.csv` file
```bash
head -n 1001 fhvhv_tripdata_2021-01.parquet > head.csv
```

Make the file executable
```bash
chmod +x <file_name>
```

- 3 means the length of number  
- 0 means filling leading 0 when the length <3  
- x mean Hex 16, d means Digits 10.
```bash
03x
03d
```

Call a `.sh` file
```bash
./<file_name.sh> <args>
```

List folder files in a tree format
```bash
tree <folder_name>
```

Return the package path
```bash
which <package_name>
```

Lambda是一种内嵌函数，类似def function
```python
lambda arguments: expression
squared = lambda x: x**2
print(squared(5)) #output: 25
```
- Convert Jupyter Notebook to Python Script
```bash
jupyter nbconvert --to=script <notebook_name>
```

