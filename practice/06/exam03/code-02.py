from pyspark import SparkSession
from pyspark.sql.functions import *

def op_windowed_groupby(df, window_duration="15 minutes", slide_duration="5 minutes"):
    df_windowed_aggregation = df.groupBy(
        window(timeColumn=df.tpep_pickup_datetime, windowDuration=window_duration, slideDuration=slide_duration),
        df.vendor_id
    ).count()
    return df_windowed_aggregation

def format_to_kafka(df, values_columns, key_columns):
    columns = df.columns

    df = df.withColumn('value', concat_ws(','*values_columns))
    if key_columns:
        df = df.withColumnRenamed(key_columns, "key")
        df = df.withColumn("key", df.key.cast('string'))

    return df.select(['key','value'])
def sink_kafka(df, topic):
    write_query = df.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092,broker:29092") \
        .outputMode('complete') \
        .option("topic", topic) \
        .option("checkpointLocation", "checkpoint") \
        .start()
    return write_query

# 假定我已经读取了kafka数据存储在df_read_kafka
df_processed = op_windowed_groupby(df_read_kafka)
df_output = format_to_kafka(df_processed, values_columns=['count'], key_columns=['vendor_id'])
sink_kafka(df_output, topic='vendor_statistics')