选择题
1. C 
2. A (这道题我不确定)
3. C （我知道他是将数据读取后，print出来）

简答题
1. acknowledgement跟node replicas属于联动关系吧，如果是0的话，producer不会等待leader and follower收到数据的confirmation, 1的话，leader node确实收到和传输数据后，就直接confirm，不会等待follower confirmation, all的话，是等leader and follower都确认收到数据并传输后，才会确认，0的传输效率最快，但丢失数据风险最高，1的话最慢，但风险最小
2. op_windowed_groupby是根据pickup_datetime and vendor_id分组，每隔五分钟计算，几分钟内的df内每个field的个数 （这道题我也不确定）
3. AvroSerializer是将数据转换成binary format, 而AvroDeserializer将数据从binary format转换成指定的格式
在我的代码中，AvroSerializer和AvroDeserializer都有自定义的dict func
AvroSerializer将数据先放到自定义的dict func里面重新format一下，然后call AvroSerializer用to_dict转换成dict格式, 再用fast avro转成binary
AvroDeserizlier先讲binary转换成字典格式，再放进from_dict里转换成自定义的字典格式

填空题
1. key （不确定）
2. 将所有的service在后台运行起来
3. writeStream

代码题
1.  
class PracticeAvroProducer:
    def __init__(self, props:Dict):
        key_schema_str = xxx
        value_schema_str = xxx
        schema_registry_props = xxx
        schema_registry_client = xxx
        self.key_serializer = AvroSerializer(schema_registry_client, key_schema_str, to_dict=None)
        self.value_serializer = AvroSerializer(schme_registry_client, key_schma_str, to_dict=None)
    
    def publish(self, topic: str, records: list()):
        for key_value in records:
        key, value = key_values
        self.producer.prouce(topic=topic,
            key = self.key_serializer(key, cxt=None),
            value = self.value_serializer(value, cxt=None))
config = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'schema_registry.url': SCHEMA_REGISTRY_URL,
    'schema.key': RIDE_KEY_SCHEMA_PATH,
    'schema.value': RIDE_VALUE_SCHEMA_PATH
}
producer = PracticeAvroProducer(props=conig)
producer.publish(topic='demo_topic', [({'key':'1'}, {"name": "Alice"}), ({'key':'2'}, {"name": "Bob"})])
2.  
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
        .filter(col('vendor_id').isin('1','2'))
        .load()
    return df_stream
3.  
df_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092,broker:29092") \
    .option("subscribe", consume_topic) \
    .option("startingOffsets", "earliest") \
    .option("checkpointLocation", "checkpoint") \
    .filter(col('vendor_id').isin('1','2'))
    .load()
df_stream.writeStream.format('csv').svae(xxx)