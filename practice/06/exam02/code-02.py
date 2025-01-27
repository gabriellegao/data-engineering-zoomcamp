import pyspark.sql.functions as F
def read_from_kafka(consume_topic: str):
    # Spark Streaming DataFrame, connect to Kafka topic served at host in bootrap.servers option
    # Read data from Kafka cluster, producing by producer.py
    df_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092,broker:29092") \
        .option("subscribe", consume_topic) \
        .option("startingOffsets", "earliest") \
        .option("checkpointLocation", "checkpoint") \
        .load()
    return df_stream

def window_groupby(df, window, slide):
    df_groupby = df.groupBy(
        F.window(df.pickup_datetime, windowDuration=window, slideDuration=slide),
        df.vendor_id
        ).count()
    return df_groupby

def sink_kafka(df, topic):
    write_query = df.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092,broker:29092") \
        .outputMode('complete') \
        .option("topic", topic) \
        .option("checkpointLocation", "checkpoint") \
        .start()
    return write_query


if __name__ == '__main__':
    df = read_from_kafka('topic')
    count = window_groupby(df, window="15 minutes", slide='5 minutes')
    sink = sink_kafka(count, topic='vendor_statistics')

    spark.streams.awaitAnyTermination()
