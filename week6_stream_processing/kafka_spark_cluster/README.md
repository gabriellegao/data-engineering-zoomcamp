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
Kafka & Spark Standalone Cluster Setup -> [docker-compose.yaml](kafka_spark_cluster/docker-compose.yaml)
