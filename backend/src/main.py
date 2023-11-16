import asyncio
import logging
import traceback
from contextlib import asynccontextmanager
from datetime import datetime

import paho.mqtt.client as mqtt
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from proto.NoiseMeasurement_pb2 import NoiseMeasurement
from src.connection import ConnectionManager
from src.database import SessionLocal, models
from src.settings import SETTINGS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mqtt_client = mqtt.Client()
manager = ConnectionManager()


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to Mosquitto with result code {rc}.")
    client.subscribe("default-topic")


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    received_at = datetime.utcnow()
    logger.info(f"Received message on topic {repr(msg.topic)} at UTC {received_at}.")

    message = NoiseMeasurement()
    message.ParseFromString(msg.payload)

    try:
        with SessionLocal() as session:
            db_measurement = models.NoiseMeasurement(
                noise_value=message.noise_value,
                room_id=message.room_id,
                device_id=message.device_id,
            )
            session.add(db_measurement)
            # session.commit()
    except Exception:
        logger.info("Error adding to database")
        traceback.print_exc()
    else:
        logger.info("Added to database")

    asyncio.run(manager.broadcast(message.room_id, message.noise_value))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start up
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.tls_set("./data/certificate.pem")
    mqtt_client.tls_insecure_set(True)
    mqtt_client.username_pw_set(SETTINGS.mosquitto_user, SETTINGS.mosquitto_password)
    mqtt_client.connect(SETTINGS.mosquitto_host, SETTINGS.mosquitto_port, 60)
    mqtt_client.loop_start()

    yield

    # Shutdown
    mqtt_client.disconnect()


app = FastAPI(lifespan=lifespan)


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await manager.connect(room_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
