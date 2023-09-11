from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
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
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=[BROKER_URL]
    )

    iteration = 0
    while True:
        producer.send(topic_name, value={"Hello": "world!", "Iteration": str(iteration)}).get(timeout=30)
        iteration += 1
        await asyncio.sleep(0.5)


async def consume(topic_name):
    """Consumes data from the Kafka Topic"""
    consumer = KafkaConsumer(
        topic_name,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-first-consumer-group',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=[BROKER_URL]
    )

    for m in consumer:
        print(m.value)
        await asyncio.sleep(0.5)


async def produce_consume():
    """Runs the Producer and Consumer tasks"""
    t1 = asyncio.create_task(produce(TOPIC_NAME))
    t2 = asyncio.create_task(consume(TOPIC_NAME))
    await t1
    await t2


def main():

    print(f"BROKER_URL: {BROKER_URL}")
    print(f"TOPIC_NAME: {TOPIC_NAME}")

    try:
        asyncio.run(produce_consume())
    except KeyboardInterrupt as e:
        print("Shutting down\n")
    finally:
        print("Handling exception...\n")


if __name__ == "__main__":
    main()
