def consume_from_kafka(self, topics: List[str], partition: int):
        self.consumer.subscribe(topics=topic, partition=partition)
        print('Consuming from Kafka started')
        print('Available topics to consume: ', self.consumer.subscription())
        while True:
            try:
                # SIGINT can't be handled when polling, limit timeout to 1 second.
                msg = self.consumer.poll(1.0)
                if msg is None or msg == {}:
                    continue
                for msg_key, msg_values in msg.items():
                    for msg_val in msg_values:
                        print(f'Key:{msg_val.key}-type({type(msg_val.key)}), '
                              f'Value:{msg_val.value}-type({type(msg_val.value)})')
            except KeyboardInterrupt:
                break

        self.consumer.close()