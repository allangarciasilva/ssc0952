import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

from proto import NoiseMeasurement_pb2
from src.settings import SETTINGS


def on_connect(client, userdata, flags, rc):
    print(f"Connected to Mosquitto with result code {rc}.")
    client.subscribe(SETTINGS.mosquitto_topic)


def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}")
    message = NoiseMeasurement_pb2.NoiseMeasurement()
    message.ParseFromString(msg.payload)
    print(message)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(SETTINGS.mosquitto_user, SETTINGS.mosquitto_password)
    client.connect(SETTINGS.mosquitto_host, SETTINGS.mosquitto_port, 60)
    client.loop_forever()


if __name__ == "__main__":
    print("Starting application")
    main()
