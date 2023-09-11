# Apache Kafka docker

## Setting up Kafka and Zookeeper with macOS Docker Desktop

This tutorial provides a step-by-step instruction on how to deploy a Kafka broker with Docker containers when a Kafka producer and consumer sit on different networks.

If you're new to the Kafka world, the [introduction](https://kafka.apache.org/documentation/#introduction) and [design](https://kafka.apache.org/documentation/#design) sections of the Apache documentation are an excellent place to start.

![Kafka-scenario](./kafka-scenario.png)

## Prerequisites

* macOS Docker Desktop

    See [Install Docker Desktop](https://docs.docker.com/docker-for-mac/install/) for download information and installation instructions.

* macOS Python 3.7 (optional)

    Check out my tutorial [mac-dev-setup](https://github.com/monsieurborges/mac-setup) to install Python on your MacBook.

## Getting Started

Here you find tutorials for two versions of Kafka configurations:

* [Wurstmeister Kafka and kafka-python](./wurstmeister/)
* [Confluent Kafka and confluent-kafka-python](./confluent/)

## References

* [Apache kafka](https://kafka.apache.org)
* [Hello Kafka World! The complete guide to Kafka with Docker and Python](https://medium.com/big-data-engineering/hello-kafka-world-the-complete-guide-to-kafka-with-docker-and-python-f788e2588cfc)
* [My Python/Java/Spring/Go/Whatever Client Won’t Connect to My Apache Kafka Cluster in Docker/AWS/My Brother’s Laptop. Please Help!](https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/)
* [Kafka Listeners - Explained](https://www.confluent.io/blog/kafka-listeners-explained/)
* [Deploy a Kafka broker in a Docker container](https://www.kaaproject.org/kafka-docker)
