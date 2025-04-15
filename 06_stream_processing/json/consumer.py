from typing import Dict, List
from json import loads
from kafka import KafkaConsumer

from ride import Ride
from settings import BOOTSTRAP_SERVERS, KAFKA_TOPIC


class JsonConsumer:
    def __init__(self, props: Dict):
        self.consumer = KafkaConsumer(**props)

    def consume_from_kafka(self, topics: List[str]):
        self.consumer.subscribe(topics)
        print('Consuming from Kafka started')
        print('Available topics to consume: ', self.consumer.subscription())
        while True:
            try:
                # SIGINT can't be handled when polling, limit timeout to 1 second.
                # Output format: binary -> TopicPartition dictionary
                message = self.consumer.poll(1.0)
                if message is None or message == {}:
                    continue
                # Output format of message_key: key in TopicPartition dictionary
                # Output format of message_value: Ride object in TopicPartition dictionary
                for message_key, message_value in message.items():
                    # Output format of msg_val: object
                    for msg_val in message_value:
                        print(msg_val.key, msg_val.value)
            except KeyboardInterrupt:
                break

        self.consumer.close()


if __name__ == '__main__':
    config = {
        'bootstrap_servers': BOOTSTRAP_SERVERS,
        'auto_offset_reset': 'earliest',
        'enable_auto_commit': True, # True意味着自动提交offset, False的话，需要手动提交并配合commit()使用
        # Convert messages from binary to int
        'key_deserializer': lambda key: int(key.decode('utf-8')),
        #Comvert messages from binary -> json -> dict -> object(list)
        'value_deserializer': lambda x: loads(x.decode('utf-8'), object_hook=lambda d: Ride.from_dict(d)),
        'group_id': 'consumer.group.id.json-example.1',
    }

    json_consumer = JsonConsumer(props=config)
    json_consumer.consume_from_kafka(topics=[KAFKA_TOPIC])