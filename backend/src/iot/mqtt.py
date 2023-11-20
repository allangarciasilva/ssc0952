import asyncio
import traceback
from datetime import datetime

from paho.mqtt import client as mqtt

from proto.NoiseMeasurement_pb2 import NoiseMeasurement
from src.connection import connection_manager
from src.database import SessionLocal, models

from src.main import logger

mqtt_client = mqtt.Client()


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

    asyncio.run(connection_manager.broadcast(message.room_id, message.noise_value))
