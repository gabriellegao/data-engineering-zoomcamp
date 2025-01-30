## Pre-requisite for Creating Clusters on Docker 
### Prepare Base Image

Instruction to prepare base image -> [README.md](../docker_env_setup/README.md)

Scripts to build base image -> [Docker Environment Setup](../docker_env_setup/)

## Create Spark and Kafaka Clusters
### Build Image: Image for Kafka and Spark Clusters
```bash
chmod +x build.sh
./build.sh
```

### Create Containers: Containers for Kafka and Spark Clusters

Instruction to create containers -> [README.md](../kafka_spark_cluster/README.md)

Scripts to create containers -> [docker-compose.yaml](../kafka_spark_cluster/docker-compose.yaml)

```bash
# Create Network
docker network create kafka-spark-network

# Start Docker-Compose (within for kafka and spark folders)
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
### Create Kafka Topic 
This command is to config Kafka topic. After running this command, we can parse topic as an argument into`producer.py` and `consumer.py`.  
```bash
docker exec -it broker kafka-topics.sh \
  --create \
  --topic rides_csv \
  --partitions 3 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092
```
We can also combine all commands into one shell script.
```bash
#!/bin/bash

TOPIC_NAME="demo_1"
BROKER="localhost:9092"

echo "🚀 Checking if topic '$TOPIC_NAME' exists..."
EXISTING_TOPIC=$(docker exec -it broker kafka-topics.sh --list --bootstrap-server $BROKER | grep $TOPIC_NAME)

if [ -z "$EXISTING_TOPIC" ]; then
  echo "📌 Topic '$TOPIC_NAME' does not exist. Creating now..."
  docker exec -it broker \
  kafka-topics.sh \ 
      --create \
      --topic $TOPIC_NAME \
      --bootstrap-server $BROKER \
      --partitions 2
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

### Run Producer and Consumer
To run `producer.py` and `consumer.py` on local machine, make sure the ports of Kafka and Schema Registry are exposed to localhost.
```bash
# Setup ports in docker-compose.yaml
services:
  broker:
    ports:
      - "9092:9092"
  schema-registry:
    ports:
      - "8081:8081"
```
```bash
# Run producer
python3 producer.py

# Run consumer with default settings
python3 consumer.py
# Run consumer for specific topic
python3 consumer.py --topic <topic-name>
```

### Run Streaming Script
- Consume data from producer
- Process streaming data using Spark DataFrame
- Write data to console or another topic of Producer
```bash
chmod +x spark-submit.sh
./spark-submit.sh streaming.py
```
## Additional Notes
除了上面提到的, 将ports暴露给主机, 在本地运行`producer.py`和`consumer.py`. 还有以下方法:
### Method1: Run `producer.py` and `consumer.py` inside Docker
Add a new service in `docker-compose.yaml`
```bash
services:
  producer-consumer:
    image: python:3.9-slim
    container_name: producer-consumer
    depends_on:
      - broker
      - schema-registry
    volumes:
      - ./pyspark:/app/scripts  # 挂载本地脚本目录
    working_dir: /app/scripts
    environment:
      - BOOTSTRAP_SERVERS=broker:9092
      - SCHEMA_REGISTRY_URL=http://schema-registry:8081
    command: ["tail", "-f", "/dev/null"]  # 防止容器退出
```
Kick off services to run python scripts
```bash
docker-compose up -d producer-consumer
docker exec -it producer-consumer bash
python3 producer.py
python3 consumer.py
```
### Method2: Create Custom Image
Prepare Dockerfile
```bash
FROM python:3.9

WORKDIR /app

# 安装依赖
RUN pip install confluent-kafka

# 复制producer.py and consumer.py
COPY . /app

CMD ["bash"]
```
Build image
```bash
docker build -t kafka-scripts .
```
Connect to docker network
```bash
docker network connect kafka-spark-network producer-container
docker network connect kafka-spark-network consumer-container
```
Create containers in `bash` commands and run two python scripts after `broker` and `schema-registry` services starts
```bash
# Producer Container
docker run --name producer-container kafka-scripts
python3 producer.py
# Consumer Container
docker run --name consumer-container kafka-script
python3 consumer.py
```
Create containers in `docker-compose.yaml`
```bash
services:
  producer:
    build:  # 使用 Dockerfile 构建镜像
      context: .
      dockerfile: Dockerfile
    container_name: producer-container
    environment:
      - BOOTSTRAP_SERVERS=broker:9092
      - SCHEMA_REGISTRY_URL=http://schema-registry:8081
      - KAFKA_TOPIC=rides_avro
    depends_on:
      - broker
      - schema-registry
    command: ["python3", "producer.py"]  # 启动时运行 producer.py

  consumer:
    build:  # 使用相同镜像
      context: .
      dockerfile: Dockerfile
    container_name: consumer-container
    environment:
      - BOOTSTRAP_SERVERS=broker:9092
      - SCHEMA_REGISTRY_URL=http://schema-registry:8081
      - KAFKA_TOPIC=rides_avro
    depends_on:
      - broker
      - schema-registry
    command: ["python3", "consumer.py"]  # 启动时运行 consumer.py
```