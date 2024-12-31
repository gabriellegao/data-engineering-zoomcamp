import pyspark
from pyspark.sql import SparkSession
import os

pyspark.__version__

spark = SparkSession.builder\
    .master("local[*]")\
    .appName('test')\
    .getOrCreate()

os.system("wget 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'")


df = spark.read\
    .option("header", "true")\
    .csv('taxi_zone_lookup.csv')

df.show()

df.write.parquet('zones')






