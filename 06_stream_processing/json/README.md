## `Json` Producer and Consumer
### Run Producer and Consumer
```bash
# Start producer script
python3 producer.py
# Start consumer script
python3 consumer.py
```
Producer -> [producer.py](producer.py)

Transformation -> [ride.py](ride.py)

Consumer -> [cosumer.py](consumer.py)

Settings -> [settings.py](settings.py)

## Consumer Data Structure
### Output from `poll()`
The structure of output is dictionary of list.  
```python
{
    TopPartition(topic,partition):[
        # Key and value are raw bytes before deserialization
        ConsumerRecord(topic, partition, offset, key, value, timestamp),
        ConsumerRecord(topic, partition, offset, key, value, timestamp),
        ...
    ],
    TopPartition(topic,partition):[
        ...
    ]
}
```
### Json Deserialization
After deserialization, the key is string and the value is dictionary.
```python
Key: 1, Value: {'vendor_id': '2'}
Key: 2, Value: {'vendor_id': '3'}
Key: 3, Value: {'vendor_id': '4'}
```
### Avro Deserialization
After deserialization, the key is integer and the value is object
```python
Key: 1, Value: RideRecord(vendor_id=2, passenger_count=3, trip_distance=10.5)
Key: 2, Value: RideRecord(vendor_id=3, passenger_count=2, trip_distance=7.8)
```
### Read Data from Assigned Partition
Use `assign()` to subscribe to the specific topic and partition
```python
consumer = KafkaConsumer()
consumer.assign([TopicPartition(topic, partition)])
```