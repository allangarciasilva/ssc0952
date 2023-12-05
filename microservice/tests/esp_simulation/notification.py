import asyncio

from proto.ESPSetup_pb2 import ESPSetup
from proto.NoiseMeasurement_pb2 import NoiseMeasurement
from src.shared.utils import create_mqtt_client


async def publish_message(device_name: str, room_id: int):
    async with create_mqtt_client() as client:
        message = ESPSetup(device_name=device_name, room_id=room_id)
        await client.publish("setup", message.SerializeToString())
        print(f"Setup sent for device {device_name} at room {room_id}.")

        total_time = 20
        delay = 0.15

        for i in range(int(total_time / delay)):
            dx = i % 3 - 1
            message = NoiseMeasurement(device_name=device_name, noise_value=10 + dx / 3)
            await client.publish("noise", message.SerializeToString())
            await asyncio.sleep(delay)

        await client.publish("shutdown", device_name)
        print(f"Shutdown sent for device {device_name} at room {room_id}.")


async def main():
    devices = [
        f"ESP32:0000.0000.0000.{i:04}"
        for i in range(200)
    ]

    print("Starting")
    async with asyncio.TaskGroup() as tg:
        for index, device_name in enumerate(devices):
            tg.create_task(publish_message(device_name, 1 + index % 4))
    print("Fisinhed")


asyncio.run(main())
