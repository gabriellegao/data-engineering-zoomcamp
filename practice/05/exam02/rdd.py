# 代码题第一题
import pyspark
from pyspark.sql import SparkSession
from datetime import datetime
from pyspark.sql.functions import length, mean
from collections import namedtuple
from pyspark.sql.types import StructType, StructField, IntegerType,StringType

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df_csv = spark.read.format('csv').option('header', True).load('path/to/csv')

df_rdd = df.rdd

def filter_rdd(row):
    return length(row.value) > 50

def grouping_rdd(row):
    return row.id

def calculating_avg(left_value, right_value):
    return (left_value + right_value)/2 #或者可以写成 mean(left_value, right_value)

naming_col = namedtuple('nameing_col', ['id','value'])

schema = StringType([
    StructField('id', StringType(), True),
    StructField('value', IntegerType(), True)
])

def name_column(row):
    return naming_col(
        id=row[0],
        value=row[1]
    )

df_results = df_rdd\
.filter(filter_rdd)\
.map(grouping_rdd)\
.reduceByKey(calculating_avg)\
.map(name_column)