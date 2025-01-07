import os
import csv
from time import sleep
from typing import Dict
# Import Kafaka-required libraries 
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
# Import Python Modules
from ride_record_key import RideRecordKey, ride_record_key_to_dict
from ride_record import RideRecord, ride_record_to_dict
from settings import RIDE_KEY_SCHEMA_PATH, RIDE_VALUE_SCHEMA_PATH, \
    SCHEMA_REGISTRY_URL, BOOTSTRAP_SERVERS, INPUT_DATA_PATH, KAFKA_TOPIC


def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed for record {}: {}".format(msg.key(), err))
        return
    print('Record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


class RideAvroProducer:
    def __init__(self, props: Dict):
        # Schema Registry and Serializer-Deserializer Configurations
        key_schema_str = self.load_schema(props['schema.key'])
        value_schema_str = self.load_schema(props['schema.value'])
        schema_registry_props = {'url': props['schema_registry.url']}
        schema_registry_client = SchemaRegistryClient(schema_registry_props)
        # AvroSerializer is a class function, required three parameters. More info in README.md
        self.key_serializer = AvroSerializer(schema_registry_client, key_schema_str, ride_record_key_to_dict)
        self.value_serializer = AvroSerializer(schema_registry_client, value_schema_str, ride_record_to_dict)

        # Producer Configuration
        producer_props = {'bootstrap.servers': props['bootstrap.servers']}
        self.producer = Producer(producer_props)

    @staticmethod
    def load_schema(schema_path: str):
        path = os.path.realpath(os.path.dirname(__file__))
        with open(f"{path}/{schema_path}") as f:
            schema_str = f.read()
        return schema_str

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            print("Delivery failed for record {}: {}".format(msg.key(), err))
            return
        # msg.key() - binary, msg.topic() - str, msg.partition() - int, msg.offset() - int
        print('Record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()))

    @staticmethod
    def read_records(resource_path: str):
        ride_records, ride_keys = [], []
        with open(resource_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # skip the header
            for row in reader: # another next()
                # Call RideRecord class and append output to list
                ride_records.append(RideRecord(arr=[row[0], row[3], row[4], row[9], row[16]]))
                # Call RideRecordKey class and append output to list
                # Input format: RideRecordKey(vendor_id=123)
                # Output format: RideRecordKey:{'vendor_id':123}
                ride_keys.append(RideRecordKey(vendor_id=int(row[0])))
        # 1 to 1 match
        """
        Output format
        [
            (RideRecordKey: {'vendor_id': 1}, RideRecord: {'arr': [1, '2023-01-01 10:00:00', '2023-01-01 10:30:00', 2, 25.50]}),
            (RideRecordKey: {'vendor_id': 2}, RideRecord: {'arr': [2, '2023-01-01 11:00:00', '2023-01-01 11:20:00', 1, 15.00]}),
            (RideRecordKey: {'vendor_id': 3}, RideRecord: {'arr': [3, '2023-01-01 12:00:00', '2023-01-01 12:45:00', 3, 30.75]})
        ]
        Even though key and value look like dict, they are still object.
        Real output format: RideRecordKey(vendor_id=123)
        """
        return zip(ride_keys, ride_records)

    def publish(self, topic: str, records: [RideRecordKey, RideRecord]):
        # Input format is the same as the zip()
        for key_value in records:
            key, value = key_value
            try:
                self.producer.produce(topic=topic,
                                      # Call __call__ func in Avro class
                                      # The format of key is an object -> dict -> binary
                                      key=self.key_serializer(key, SerializationContext(topic=topic,
                                                                                        field=MessageField.KEY)),
                                      value=self.value_serializer(value, SerializationContext(topic=topic,
                                                                                              field=MessageField.VALUE)),
                                      on_delivery=delivery_report)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Exception while producing record - {value}: {e}")

        self.producer.flush()
        sleep(1)


if __name__ == "__main__":
    config = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'schema_registry.url': SCHEMA_REGISTRY_URL,
        'schema.key': RIDE_KEY_SCHEMA_PATH,
        'schema.value': RIDE_VALUE_SCHEMA_PATH
    }
    producer = RideAvroProducer(props=config)
    ride_records = producer.read_records(resource_path=INPUT_DATA_PATH)
    producer.publish(topic=KAFKA_TOPIC, records=ride_records)