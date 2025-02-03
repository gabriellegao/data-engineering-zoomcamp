from pyspark.sql import SparkSessopm
from pyspark.sql.functions import *

def read_from_kafka(consume_topic):
    df_stream = spark.readStream \
                    .format('kafka') \
                    .option("kafka.bootstrap.servers", "localhost:9092,broker:29092") \
                    .option("subscribe", consume_topic) \
                    .option('startingOffsets','earliest') \
                    .option('checkpointLocation','checkpoint') \
                    .load
    return df_stream

def sink_console(df, output_mode, processing_time):
    write_console = df.writeStream \
                    .outputMode(output_mode) \
                    .trigger(processing_time) \
                    .format('console') \
                    .option('truncate',False) \
                    .start()
    return write_console
# explain what is .option('truncate',False)

if __name__ == '__main__':
    spark=SparkSession,builder.appName('code-01').getOrCreate()

    df_consume_stream = read_from_kafka('vendor_statistics')
    sink_console(df_consume_stream, output_mode='complete',processing_time="20 seconds")

# explain output mode, what options we have for output mode?