from pyspark.sql import SparkSession
from pyspark.sql.functions import *

def read_from_kafka(consume_topc):
    df_stream=spark.readStream \
        .format('kafka') \
        .option('kafka.bootstrap.server', 'localhost:9092, broker:29092') \
        .option('subscribe',consume_topc) \
        .option('startOffsets','earliest') \
        .option('checkpointLocation','checkpoint') \
        .load()
    return df_stream

def parse_from_kafka(df, schema):
    assert df.isStreaming is True, "Doesn't receive kafka data"
    result = {}
    df = df.selectExpr("cast(key as string)", "cast(value as string)")

    col = split(df['value'], ',')

    for idx, field in enumerate(schema):
        result[field.name] = col.getItem(idx).cast(field.dataType)
    return result.to_json() 

def write_to_csv(df):
    write_query = df.writeStream \
                .format('csv') \
                .save('path/to/folder')