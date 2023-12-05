import asyncio
import ssl
import socket

import aiomqtt
import uvloop
from aiokafka import AIOKafkaProducer
from orjson import orjson

from proto.ESPSetup_pb2 import ESPSetup
from proto.NoiseMeasurement_pb2 import NoiseMeasurement
from src.shared.settings import SETTINGS
from src.shared.utils import create_mqtt_client


def key_partitioner(key, _all_partitions, available_partitions):
    index = abs(hash(key)) % len(available_partitions)
    return available_partitions[index]


async def dispatch_message(kafka_producer: AIOKafkaProducer, message: aiomqtt.Message):
    if message.topic.matches("setup"):
        content = ESPSetup()
        content.ParseFromString(message.payload)
        print(f"Device {content.device_name} setup.")
        await kafka_producer.send("setup", key=content.device_name.encode(),
                                  value=orjson.dumps({"room_id": content.room_id}))

    elif message.topic.matches("shutdown"):
        device_name = message.payload.decode()
        print(f"Device {device_name} shutdown.")
        await kafka_producer.send("shutdown", key=device_name.encode())

    elif message.topic.matches("noise"):
        content = NoiseMeasurement()
        content.ParseFromString(message.payload)
        await kafka_producer.send("noise", key=content.device_name.encode(),
                                  value=orjson.dumps(content.noise_value))


async def read_mqtt_messages(message_queue: asyncio.Queue[aiomqtt.Message]):
    async with create_mqtt_client() as client:
        async with client.messages() as messages:
            await client.subscribe("setup")
            await client.subscribe("shutdown")
            await client.subscribe("noise")
            async for message in messages:
                await message_queue.put(message)


async def publish_messages_to_kafka(message_queue: asyncio.Queue[aiomqtt.Message]):
    kafka_producer = AIOKafkaProducer(bootstrap_servers=SETTINGS.kafka_server, partitioner=key_partitioner)
    await kafka_producer.start()

    try:
        while True:
            message = await message_queue.get()
            await dispatch_message(kafka_producer, message)
    finally:
        await kafka_producer.stop()


async def main():
    queue = asyncio.Queue()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(read_mqtt_messages(queue))
        tg.create_task(publish_messages_to_kafka(queue))


if __name__ == "__main__":
    print("Starting MQTT-Kafka bridge")
    try:
        uvloop.run(main())
    except KeyboardInterrupt:
        print("Stopping MQTT-Kafka bridge")
