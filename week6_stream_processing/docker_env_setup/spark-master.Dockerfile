# Inherit everything from spark-base image
FROM spark-base

# -- Runtime

# Create a build-time environment variable
ARG spark_master_web_ui=8080

EXPOSE ${spark_master_web_ui} ${SPARK_MASTER_PORT}
# CMD: Define default command
# bin/spark-class org.apache.spark.deploy.master.Master: Call Java class
# logs/spark-master.out: Write log to this location
CMD bin/spark-class org.apache.spark.deploy.master.Master >> logs/spark-master.out