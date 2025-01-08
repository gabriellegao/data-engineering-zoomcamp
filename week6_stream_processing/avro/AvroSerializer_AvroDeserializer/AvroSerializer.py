import struct
import io
from fastavro import schemaless_writer
from confluent_kafka.schema_registry import SchemaRegistryClient

MAGIC_BYTE = 0  # Kafka Avro 消息的 Magic Byte 固定为 0

class AvroSerializer:
    def __init__(self, schema_registry_client, schema_str, to_dict=None):
        self.schema_registry_client = schema_registry_client
        self.schema = schema_str  # 传入的 Avro Schema
        self.to_dict = to_dict  # 自定义序列化函数（用于处理 Python 自定义对象）

        # 获取或注册 Schema ID
        self.schema_id = self.get_schema_id(schema_str)

    def get_schema_id(self, schema_str):
        """
        与 Schema Registry 交互，获取或注册 Schema ID
        """
        subject = "your_topic-value"
        schema_id = self.schema_registry_client.get_latest_version(subject).schema_id
        return schema_id  # 获取 Schema ID

    def __call__(self, obj, ctx):
        """
        序列化 Python 对象为 Avro 二进制格式，并添加 Kafka Avro Header
        """
        if self.to_dict is not None:
            obj = self.to_dict(obj, ctx)  # 调用自定义序列化函数，转换为字典格式

        # 1️⃣ 使用 FastAvro 进行 Avro 序列化
        bytes_writer = io.BytesIO()
        schemaless_writer(bytes_writer, self.schema, obj)
        avro_data = bytes_writer.getvalue()

        # 2️⃣ 生成 Kafka 消息格式：Magic Byte (1 byte) + Schema ID (4 bytes) + Avro Data
        return struct.pack('>bI', MAGIC_BYTE, self.schema_id) + avro_data
