## Apache Kafka
### What is Apache Kafka
Apache Kafaka is a distributed event streaming platform desiged to handle high-throughput, fault-tolerant, real-time data processing.
- Producers: write events to Kafka topics
- Topics: categories that receive and store messages/records/events
- Broker (Node): servers to store and distribute data
- Consumer: subscribe to topics, receive events
- Zookeeper(retired): manage metadata and coordinate brokers

### Messages/Events Structure
The common components of message in topic are key, value and timestamp. 

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
Kafka topics are divided into partitions.  
One partition is consumed by only one consumer/consumer group.  
One consumer can read from multiple partitions.  
If one consumer fails, Kafaka will direct the partition to another consumer in the same consumer group.  

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

## Create Standalone Spark Cluster on Docker
