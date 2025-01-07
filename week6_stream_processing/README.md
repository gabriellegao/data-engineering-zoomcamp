## Apache Kafka
### What is Apache Kafka
Apache Kafaka is a distributed event streaming platform desiged to handle high-throughput, fault-tolerant, real-time data processing.
- Producers: write events to Kafka topics
- Topics: categories that receive and store messages/records/events
- Broker (Node): servers to store and distribute data
- Consumer: subscribe to topics, receive events
- Zookeeper(retired): manage metadata and coordinate brokers

### Messages/Events Structure
The components of message in topic are topic, key, value , partition, offset and timestamp.  
Only key and value are serialized to binary format.  

### Replication
Kafka Clusters are composed by several nodes.  
Producers send messages to nodes of a cluster. Nodes process data and write output to Consumers.  
Replication is designed to replicate partitions among nodes.  
Every partition has one leader and multiple followers.  
- Leader: handle read and write operations and sync data to followers
- Follower: stored copies of data. If leader fails, Kafka elects one follower as a leader

### Retention
Remove messages/events older than certain days 

### Partition
#### Consumer and Partition   
One partition is consumed by only one consumer/consumer group.  
One consumer can read from multiple partitions.  
If one consumer fails, Kafaka will direct the partition to another consumer in the same consumer group.  
#### Partition and Key
Messages in Kafka topics are divided into partitions using keys.
The formula below determins which partition layer the message should go to.
```bash
partition = hash(key) % number_of_partitions
```


### Offset
The offset is the order of messages in a partition, like 0,1,2... 
After consuming messages, Consumers return log info `__consumer_offset` back to Kafka internal topics.  
```python
# Structure of __consumer_offset
(consumer_group_id, topic, partition, offset)
``` 

### Auto.Offset.Reset
Auto Offset Reset has two features:
- Latest: read next message of previous offset
- Earliest: read the first offset message

### Acknowledgement
Acks is producer configuration setting that determines how many nodes replicas must acknowledge a message before it is consider successfully written.
- Acks 0: Producer doesn't wait for acknowledgement 
- Acks 1: Leader node acknolwdge write before sending data to followers.
- Acks All: Leader node and follower nodes acknowledge write.

## Pre-requisite for Standalone Spark Cluster on Docker
### Environments 
To setup the Apache Spark in standalone mode using Docker, the following software stacks are required:
- Python 3.7 with PySpark 3.0.0
- Java 8
- Apache Spark 3.0.0 with one master and two worker nodes
- JupyterLab IDE 2.1.5
- Simulated HDFS 2.7
- Docker
- Docker Compose

### Cluster-Base Dockerfile
This file defines a foundational docker image based on Java and Python.  
Link: [cluster-base.Dockerfile](spark_java_python_docker/cluster-base.Dockerfile)

### Spark-Base Dockerfile
This file builds on cluster-base image and add Apache Spark and Hadoop.  
Link: [spark-base.Dockerfile](spark_java_python_docker/spark-base.Dockerfile)

### Spark Master Dockerfile
This file builds on spark-base image and set up a Spark Master Node.  
Link: [spark-master.Dockerfile](spark_java_python_docker/spark-master.Dockerfile)

### Spark Worker Dockerfile
This file builds on spark-base image and set up Spark Worker Nodes.  
Link: [spark-worker.Dockerfile](spark_java_python_docker/spark-worker.Dockerfile)

### JupyterLab Dockerfile
This file builds on cluster-base image and install JupyterLab and PySpark.  
Link: [jupyterlab.Dockerfile](spark_java_python_docker/jupyterlab.Dockerfile)

### Build Shell Command
Build above images.  
Link: [build.sh](spark_java_python_docker/build.sh)

### *Attention*
*Run `build.sh` first to build all custom images, then run `docker-compose.yaml` to create containers.*

## Create Spark Standalone and Kafka Cluster
### Build Base Image for Sparkalone Cluster 
```bash
# Build Spark Images
./build.sh 
```
### Create Network and Volume
```bash
# Create Network
docker network  create kafka-spark-network

# Create Volume
docker volume create --name=hadoop-distributed-file-system
```
### Run Containers on Docker
```bash
# Start Docker-Compose (within for kafka and spark folders)
docker compose up -d
```

### Stop Containers on Docker
```bash
# Stop Docker-Compose (within for kafka and spark folders)
docker compose down
```

### Helpful Commands
```bash
# Delete all Containers
docker rm -f $(docker ps -a -q)

# Delete all volumes
docker volume rm $(docker volume ls -q)
```

### Docker-Compose
- Kafka Cluster Setup ->  [docker-compose.yaml](kafka_cluster/docker-compose.yaml)
- Kafka & Spark Standalone Cluster Setup -> [docker-compose.yaml](kafka_spark_cluster/docker-compose.yaml)


## `Json` Producer and Consumer
### Run Producer and Consumer
```bash
# Start producer script
python3 producer.py
# Start consumer script
python3 consumer.py
```
Producer -> [producer.py](json/producer.py)

Transformation -> [ride.py](json/ride.py)

Consumer -> [cosumer.py](json/consumer.py)

Settings -> [settings.py](json/settings.py)

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

## Additional Notes
### Pass Args to Shell Script
#### Method 1: `--build-arg`
```bash
spark_version="3.2.0"

docker build \
    --build-arg spark_version="$spark_version" \
    -t <image_name> .
```
#### Method 2: Using Shell Variables
Build shell script without manually passing arguments 
```bash
#!/bin/bash
set -e  # Exit if any command fails

spark_version=$1  # Get first argument
hadoop_version=$2  # Get second argument

docker build \
  --build-arg spark_version="$spark_version" \
  --build-arg hadoop_version="$hadoop_version" \
  -t spark-base .
```
Call shell script with args
```bash
# First argument: 3.2.0
# Second argument: 2.7
bash build.sh 3.2.0 2.7
```

#### Method 3: Using Environment Variable
Export environment variables
```bash
export SPARK_VERSION=3.2.0
export HADOOP_VERSION=2.7
```
Build shell script without manually passing arguments
```bash
docker build \
  --build-arg spark_version="$SPARK_VERSION" \
  --build-arg hadoop_version="$HADOOP_VERSION" \
  -t spark-base .
```
#### Method 4: Using `.env` File
Add variables in `.env` file
```bash
# .env file
SPARK_VERSION=3.2.0
HADOOP_VERSION=2.7
```
Build shell script and read variables from `.env`
```bash
export $(grep -v '^#' .env | xargs)  # Load variables from .env
docker build \
  --build-arg spark_version="$SPARK_VERSION" \
  --build-arg hadoop_version="$HADOOP_VERSION" \
  -t spark-base .
```
