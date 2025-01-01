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
1. Define Schema
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
2. Print Schema
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

3 means the length of number  
0 means filling leading 0 when the length <3  
x mean Hex 16, d means Digits 10.
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
   - Reshuffling, moving outputs from each partition to next partition.
   - In each new partition, the records are sorted and have the same groupby
   - The algorithm of Reshuffling is called External Merge Sort
  
Stage 2 
   - Place the same groupby into one block.
  
### Spark Join
Stage 1
    - Process data and generate keys (join keys) for each record

Intermediate Stage
    - Reshuffling, place the same keys into new partitions
  
Stage 2
    - Combine record with the same key into one row

### Spark Broadcast
Broadcast happens when joining a small dataframe.  
Each Worker Nodes copy the entire small dataframe and the join happens in memory.
