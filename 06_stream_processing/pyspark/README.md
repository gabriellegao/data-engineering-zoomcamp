## Pre-requisite 
### Build Base Image

Instruction to prepare base image -> [README.md](../docker_env_setup/README.md)

Script to build base image -> [Docker Environment Setup](../docker_env_setup/)

```bash
./build.sh
```
### Create Containers for Kafka and Spark Clusters

Instruction to create containers -> [README.md](../kafka_spark_cluster/README.md)

Script to create containers -> [docker-compose.yaml](../kafka_spark_cluster/docker-compose.yaml)

```bash
# Create Network
docker network  create kafka-spark-network

# Start Docker-Compose (within for kafka and spark folders
docker-compose up -d

# Stop Docker-Compose (within for kafka and spark folders)
docker compose down
```

### Helpful Commands
```bash
docker volume ls # should list hadoop-distributed-file-system
docker network ls # should list kafka-spark-network 
```

## Pyspark Streaming Processing
### Run Producer and Consumer
```bash
# Run producer
python3 producer.py

# Run consumer with default settings
python3 consumer.py
# Run consumer for specific topic
python3 consumer.py --topic <topic-name>
```

### Run Streaming Script
```bash
./spark-submit.sh streaming.py 
```

### Create Kafka Topic 
This command is to config Kafka topic. After running this command, we can parse topic as an argument into`producer.py` and `consumer.py`.  
```bash
./bin/kafka-topics.sh \ 
    --create \
    --topic demo_1 \ 
    --bootstrap-server localhost:9092 \
    --partitions 2 \
```
We can also combine all commands into one shell script.
```bash
#!/bin/bash

TOPIC_NAME="demo_1"
BROKER="localhost:9092"

echo "🚀 Checking if topic '$TOPIC_NAME' exists..."
EXISTING_TOPIC=$(docker exec -it kafka-container kafka-topics.sh --list --bootstrap-server $BROKER | grep $TOPIC_NAME)

if [ -z "$EXISTING_TOPIC" ]; then
  echo "📌 Topic '$TOPIC_NAME' does not exist. Creating now..."
  docker exec -it kafka-container kafka-topics.sh --create --topic $TOPIC_NAME --bootstrap-server $BROKER --partitions 2
  echo "✅ Topic '$TOPIC_NAME' created."
else
  echo "✅ Topic '$TOPIC_NAME' already exists."
fi

echo "🚀 Starting Kafka Producer..."
python producer.py --topic $TOPIC_NAME &  # Run producer in the background

sleep 3  # Wait for producer to send some messages

echo "🚀 Starting Kafka Consumer..."
python consumer.py --topic $TOPIC_NAME  # Run consumer

echo "✅ Kafka Streaming process completed."
```