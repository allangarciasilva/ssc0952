import asyncio
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.shared.auth.crud import LoggedUserWs
from src.shared.settings import SETTINGS
from src.shared.utils import run_app

app = FastAPI()


async def filter_by_key(key: str | bytes, consumer: AIOKafkaConsumer):
    if isinstance(key, str):
        key = key.encode()

    async for message in consumer:
        if message.key == key:
            yield message


@app.websocket("/ws/user/")
async def websocket_endpoint(websocket: WebSocket, user: LoggedUserWs):
    consumer = AIOKafkaConsumer('notification', bootstrap_servers=SETTINGS.kafka_server)
    await consumer.start()

    async def reader():
        async for msg in filter_by_key(str(user.id), consumer):
            await websocket.send_text(msg.value.decode())

    await websocket.accept()
    reader_task = asyncio.create_task(reader())

    try:
        while True:
            await websocket.receive_bytes()
    except WebSocketDisconnect:
        reader_task.cancel()
        await consumer.stop()


@app.websocket("/ws/noise/{device_name}")
async def websocket_endpoint(device_name: str, websocket: WebSocket, user: LoggedUserWs):
    consumer = AIOKafkaConsumer('noise', bootstrap_servers=SETTINGS.kafka_server)
    await consumer.start()

    async def reader():
        async for msg in filter_by_key(device_name, consumer):
            await websocket.send_text(msg.value.decode())

    await websocket.accept()
    reader_task = asyncio.create_task(reader())

    try:
        while True:
            await websocket.receive_bytes()
    except WebSocketDisconnect:
        reader_task.cancel()
        await consumer.stop()


if __name__ == "__main__":
    run_app("src.web_message_streamer.main:app", 8081)
