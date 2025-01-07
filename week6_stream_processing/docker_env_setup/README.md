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