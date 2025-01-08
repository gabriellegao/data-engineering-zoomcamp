import struct
import io
from fastavro import schemaless_reader
from confluent_kafka.schema_registry import SchemaRegistryClient

MAGIC_BYTE = 0  # Kafka Avro 消息的 Magic Byte 固定为 0

class AvroDeserializer:
    def __init__(self, schema_registry_client, schema_str, from_dict=None):
        """
        AvroDeserializer 负责将 Avro 二进制数据解析回 Python 对象
        :param schema_registry_client: Schema Registry 客户端
        :param schema_str: Avro Schema 字符串
        :param from_dict: 自定义字典 -> Python 对象的转换函数（可选）
        """
        self.schema_registry_client = schema_registry_client
        self.schema = schema_str  # Avro Schema
        self.from_dict = from_dict  # 用户提供的 dict 转换函数（用于还原对象）

    def __call__(self, value, ctx):
        """
        反序列化 Avro 二进制数据
        :param value: Kafka 消息的 key 或 value（Avro bytes）
        :param ctx: SerializationContext，包含 topic 和 field 信息
        :return: 解析后的 Python 对象（如果 `from_dict` 存在，则转换成对象）
        """
        if value is None:
            return None

        # 解析 Avro 数据
        obj_dict = self.deserialize(value)  # Avro `bytes` -> `dict`

        # 需要转换成 Python 对象
        if self.from_dict is not None:
            return self.from_dict(obj_dict, ctx)
        return obj_dict  # 如果没有 `from_dict`，直接返回 `dict`

    def deserialize(self, value):
        """
        解析 Avro 二进制数据
        :param value: Avro `bytes`
        :return: `dict`
        """
        if len(value) < 5:
            raise ValueError("Avro message is too short!")

        # 解析 Kafka 消息头部：[Magic Byte] + [Schema ID]
        magic, schema_id = struct.unpack('>bI', value[:5])

        if magic != MAGIC_BYTE:
            raise ValueError(f"Unknown magic byte: {magic}")

        # 解析 Avro 数据部分
        bytes_reader = io.BytesIO(value[5:])
        obj_dict = schemaless_reader(bytes_reader, self.schema)
        return obj_dict
