import asyncio
import json
import logging
import traceback
from datetime import datetime

from paho.mqtt import client as mqtt

from proto.ESPSetup_pb2 import ESPSetup
from proto.NoiseMeasurement_pb2 import NoiseMeasurement
from src.connection import connection_manager
from src.database import SessionLocal, models
from src.settings import SETTINGS

MQTT_STARTUP_TOPIC = "setup"
MQTT_SHUTDOWN_TOPIC = "shutdown"
MQTT_MEASUREMENT_TOPIC = "noise"


def get_mqtt_logger():
    logger = logging.getLogger(__name__)
    fh = logging.FileHandler(f"log/{__name__}.txt")
    logger.setLevel(logging.INFO)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    return logger


logger = get_mqtt_logger()
mqtt_client = mqtt.Client()


def on_device_connect(payload: bytes):
    message = ESPSetup()
    message.ParseFromString(payload)

    logger.info(f"Device connected: {message.device_name}. Room: {message.room_id}.")
    asyncio.run(
        connection_manager.on_device_setup(message.device_name, message.room_id)
    )


def on_device_disconnect(payload: bytes):
    device_name = payload.decode()

    logger.info(f"Device disconnected: {device_name}.")
    asyncio.run(connection_manager.on_device_shutdown(device_name))


def on_noise_received(payload: bytes):
    message = NoiseMeasurement()
    message.ParseFromString(payload)

    # logger.info(f"Received {message.noise_value} from {message.device_name}.")
    asyncio.run(
        connection_manager.publish(f"noise/{message.device_name}", message.noise_value)
    )


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to Mosquitto with result code {rc}.")
    client.subscribe(MQTT_MEASUREMENT_TOPIC)
    client.subscribe(MQTT_STARTUP_TOPIC)
    client.subscribe(MQTT_SHUTDOWN_TOPIC)


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    if msg.topic == MQTT_STARTUP_TOPIC:
        on_device_connect(msg.payload)
    if msg.topic == MQTT_SHUTDOWN_TOPIC:
        on_device_disconnect(msg.payload)
    if msg.topic == MQTT_MEASUREMENT_TOPIC:
        on_noise_received(msg.payload)


def setup_mqtt():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.tls_set("./data/certificate.pem")
    mqtt_client.tls_insecure_set(True)
    mqtt_client.username_pw_set(SETTINGS.mosquitto_user, SETTINGS.mosquitto_password)
    mqtt_client.connect(SETTINGS.mosquitto_host, SETTINGS.mosquitto_port, 60)
    mqtt_client.loop_start()


def shutdown_mqtt():
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
