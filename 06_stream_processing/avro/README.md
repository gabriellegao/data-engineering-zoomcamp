## `Avro` Producer and Consumer
### Run Producer and Consumer
```bash
# Start producer script
python3 producer.py
# Start consumer script
python3 consumer.py
```
Producer Python Script -> [producer.py](avro/producer.py)  

Transformation Python Script -> [ride_record_key.py](avro/ride_record_key.py) & [ride_recod.py](avro/ride_record.py)  

Consumer -> [consumer.py](avro/consumer.py)  

Settings -> [settings.py](avro/settings.py)

### AvroSerializer Class
Underlying Logic -> [AvroSerializer.py](AvroSerializer_AvroDeserializer/AvroSerializer.py)  

AvroSerializer Class is composed by three def functions.  
- `__init__(self, schema_registry_client, schema_str, to_dict=None)`
- `get_schema_id(self, schema_str)`
- `__call__(self, obj, ctx)`  

Call AvroSerializier in Python
```python
# Create a instance
avro_serializer = AvroSerializer(schema_registry_client, schema_str, to_dict)

# Aplly object into instance
serialized_data = avro_serializer(obj, SerializationContext(topic, MessageField.VALUE))

# Output values are in binary format
```

### AvroDerializer Class
Underlying Logic -> [AvroDeserializer.py](AvroSerializer_AvroDeserializer/AvroDeserializer.py)

AvroDeserializer Class is composed by three def functions.  
- `__init__(self, schema_registry_client, schema_str, from_dict=None)`
- `__call__(self, value, ctx)`
- `deserialize(self, value)`

Call AvroDeserializer in Python
```python
# Create a instance
avro_deserializer = AvroDeserializer(schema_registry_client, schema_str, from_dict)

# Aplly object into instance
deserialized_data = avro_deserializer(obj, SerializationContext(topic, MessageField.VALUE))

# Output values are in object:{dict} format
```

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