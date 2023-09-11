from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
from sys import platform
import asyncio

"""
Configure BROKER_URL and TOPIC_NAME according to the host that runs the script

docker-compose.yml
    KAFKA_ADVERTISED_LISTENERS:
        HOST_NET://localhost:9092
        DOCKER_NET://kafka:9093
"""
if platform == "linux":
    # Docker container Python
    BROKER_URL = "kafka:9093"
    TOPIC_NAME = "topic-container"

elif platform == "darwin":
    # macOS
    BROKER_URL = "localhost:9092"
    TOPIC_NAME = "topic-macos"


async def produce(topic_name):
    """Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers": BROKER_URL})

    iteration = 0
    while True:
        p.produce(topic_name, f"iteration {iteration}")
        iteration += 1
        await asyncio.sleep(1)


async def consume(topic_name):
    """Consumes data from the Kafka Topic"""
    settings = {
        'bootstrap.servers': BROKER_URL,
        'group.id': 'my-first-consumer-group',
        'client.id': 'client-1',
        'enable.auto.commit': True,
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'}
    }

    c = Consumer(settings)

    c.subscribe([topic_name])

    try:
        while True:
            message = c.poll(1.0)
            if message is None:
                print("No message received by consumer")
            elif message.error() is not None:
                print(f"Error from consumer {message.error()}")
            else:
                print(f"Consumed message {message.key()}: {message.value()}")
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        c.close()


async def produce_consume():
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(TOPIC_NAME))
    t2 = asyncio.create_task(consume(TOPIC_NAME))
    await t1
    await t2


def main():
    # Configure the AdminClient
    client = AdminClient({"bootstrap.servers": BROKER_URL})

    # Create a NewTopic object
    topic = NewTopic(TOPIC_NAME, num_partitions=1, replication_factor=1)

    # Create the topic
    client.create_topics([topic])

    print(f"BROKER_URL: {BROKER_URL}")
    print(f"TOPIC_NAME: {TOPIC_NAME}")

    try:
        asyncio.run(produce_consume())
    except KeyboardInterrupt as e:
        print("Shutting down\n")
    finally:
        client.delete_topics([topic])
        print("Handling exception...\n")


if __name__ == "__main__":
    main()
