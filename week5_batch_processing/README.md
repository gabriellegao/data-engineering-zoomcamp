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
--> In the same folder as `java`

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
export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"

## Config PySpark
### Define `PYTHONPATH` AND Add It to `PATH`
```bash
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```


## Jupyter Notebook
### Download Taxi Zone Data
```bash
!wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```
--> Download this file in Jupyter Notebook
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
### Port
Add port 4040 to port pannel in vscode. This port links to Spark Job webppage.

### Additional Notes
```bash
ls -a
```
--> List all the file including hidden one

```bash
ls -lh
```
--> List is extended list, listing file's size, access, modified date, etc.

```bash
wc -l <file_name>
```
--> Return the row count of file

```bash
head -n 1001 fhvhv_tripdata_2021-01.parquet > head.csv
```
--> Save the firt 1001 rows to `head.csv` file