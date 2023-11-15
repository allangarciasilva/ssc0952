import traceback
from contextlib import asynccontextmanager
from datetime import datetime

import paho.mqtt.client as mqtt
from fastapi import FastAPI

from proto.NoiseMeasurement_pb2 import NoiseMeasurement
from src.database import SessionLocal, models
from src.settings import SETTINGS

app = FastAPI()
mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print(f"Connected to Mosquitto with result code {rc}.")
    client.subscribe("default-topic")


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    received_at = datetime.utcnow()
    print(f"Received message on topic {repr(msg.topic)} at UTC {received_at}.")

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
            session.commit()
    except Exception:
        print("Error adding to database")
        traceback.print_exc()
    else:
        print("Added to database")


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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
