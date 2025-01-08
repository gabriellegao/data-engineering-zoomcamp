# Reference from offical Apache Spark repository Dockerfile for Kubernetes
# https://github.com/apache/spark/blob/master/resource-managers/kubernetes/docker/src/main/dockerfiles/spark/Dockerfile
ARG java_image_tag=17-jre
FROM eclipse-temurin:${java_image_tag}

# -- Layer: OS + Python
# Create a build-time environment, only use for creating image and container
ARG shared_workspace=/opt/workspace

RUN mkdir -p ${shared_workspace} && \
    apt-get update -y && \
    apt-get install -y python3 && \
    # Link python and python3
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*
# Create a run-time environment, only use when container is active.
ENV SHARED_WORKSPACE=${shared_workspace}

# -- Runtime

# Specify mouting path (inside container)
VOLUME ${shared_workspace}
CMD ["bash"]