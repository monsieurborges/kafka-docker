# Setting up Confluent Kafka and confluent-kafka-python

We are going to use these two docker images:

* [confluentinc/cp-kafka
](https://hub.docker.com/r/confluentinc/cp-kafka)
* [confluentinc/cp-zookeeper](https://hub.docker.com/r/confluentinc/cp-zookeeper)

Check out the `docker-compose.yml` file:

```dockerfile
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    container_name: cp-zookeeper
    networks:
      - kafka_network
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
  kafka:
    image: confluentinc/cp-kafka:latest
    container_name: cp-kafka
    depends_on:
      - zookeeper
    networks:
      - kafka_network
    ports:
      - 9092:9092
    expose:
      - 9093
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: DOCKER_NET://kafka:9093,HOST_NET://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: DOCKER_NET:PLAINTEXT,HOST_NET:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: DOCKER_NET
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CONFLUENT_SUPPORT_METRICS_ENABLE: 0
networks:
  kafka_network:
    name: cp-kafka
    driver: bridge
```

Start Kafka and Zookeeper dockers:

```bash
docker-compose up -d
```

Check if the processes are running:

```bash
docker-compose ps
```

Check Zookeeper logs:

```bash
docker-compose logs zookeeper | grep -i binding
```

Check Kafka broker logs:

```bash
docker-compose logs kafka | grep -i started
```

## Kafka Hello world from Python container

Check out the `Dockerfile` for the Python container:

```dockerfile
# Docker Base Image
###########################################################
FROM ubuntu:20.04

LABEL maintainer="Monsieur Borges"
LABEL version="1.0"
LABEL date="2020-06-18"

WORKDIR /workspace

ADD ./requirements.txt /workspace
ADD ./produce_consume.py /workspace

# Create a new Docker Image
###########################################################
ENV DEBIAN_FRONTEND noninteractive
RUN echo "Welcome to the World baby!"\
    # Install dependencies
    #----------------------------------------------------------
    && apt-get update \
    && apt-get --yes --quiet dist-upgrade \
    && apt-get install --yes --quiet --no-install-recommends \
        python3.7 \
        python3-pip \
        librdkafka-dev \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r /workspace/requirements.txt
```

Build the Docker image:

```bash
docker build --rm --tag cp-kafka-app-py .
```

Run the `produce_consume.py` script inside the Docker container:

```bash
docker run --rm -it --network cp-kafka \
    cp-kafka-app-py:latest \
    python3 produce_consume.py
```

## Kafka Hello world from macOS

> Check out my tutorial [mac-dev-setup](https://github.com/monsieurborges/mac-setup) to install Python on your MacBook.

Create a Python virtual environment:

```bash
mkvirtualenv cp-kafka
```

Install the requirements:

```bash
# https://docs.confluent.io/3.1.1/installation.html#cpp-client
# Linux: sudo apt-get install librdkafka-dev
brew install librdkafka
```

```bash
pip install confluent-kafka
```

Run the `produce_consume.py` script from your macOS:

```bash
python produce_consume.py
```

## Clean up everything

Stop Kafka cluster:

```bash
docker-compose down --volumes
```

Remove Docker images:

```bash
docker image rmi \
    cp-kafka-app-py:latest \
    ubuntu:20.04 \
    confluentinc/cp-kafka:latest \
    confluentinc/cp-zookeeper:latest
```

Remove Python virtual environment:

```bash
rmvirtualenv cp-kafka
```

## References

* [Introduction to Apache Kafka for Python Programmers](https://www.confluent.io/blog/introduction-to-apache-kafka-for-python-programmers/)
* [The Apache Kafka C/C++ library](https://github.com/edenhill/librdkafka)
* [Confluent's Kafka Python Client](https://github.com/confluentinc/confluent-kafka-python)
* [Confluent Kafka client installation for C/C++ and Python](https://docs.confluent.io/3.1.1/installation.html#cpp-client)
* [Confluent Documentation](https://docs.confluent.io/current/)
