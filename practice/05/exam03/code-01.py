import pyspark
from pyspark.sql import SparkSession
from datetime import datetime

import pandas as pd
import numpy as np

from collections import namedtuple

spark=SparkSession.builder \
.appName('code-01') \
.getOrCreate()

df = spark.read.format('csv').option('header', True).load('my_file.csv').rdd

def filter_more_than_ten(series):
    return series.value > 10

def group_by_key(series):
    key = series.id
    amount = series.value
    count = 1
    value = (amount, count)

    return (key, value)

def calculate_sum(left_values, right_values):
    left_count, left_amount = left_values
    right_count, right_amount = right_values

    output_amount = left_amount + right_amount
    output_count = left_count + right_count

    return (output_amount, output_count)

row_name_func = namedtuple('row_name_func', ['id','amount','count'])

def add_cloumn_names(series):
    return row_name_func(
        id = series[0],
        amount = series[1][0],
        count = series[1][1]
    )

df_rdd = df \
.filter(filter_more_than_ten) \
.map(group_by_key) \
.reduceByKye(calculate_sum) \
.map(add_cloumn_names) \
.toDF()

df_rdd.write.format('parquet').save('path/to/folder')
print('generating parquet file....')

