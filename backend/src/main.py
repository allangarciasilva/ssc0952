import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from proto import NoiseMeasurement_pb2
from src.settings import SETTINGS

load_dotenv()


def on_message(client, userdata, message):
    decoded = NoiseMeasurement_pb2.NoiseMeasurement()
    decoded.ParseFromString(message.payload)
    print({"room_id": decoded.room_id, "device_id": decoded.device_id, "noise_value": decoded.noise_value})


def main():
    client = mqtt.Client("mqtt-subscriber")
    client.on_message = on_message

    client.username_pw_set(SETTINGS.mosquitto_user, SETTINGS.mosquitto_password)
    print(SETTINGS.mosquitto_host, 1883, 60)
    client.connect(SETTINGS.mosquitto_host, 1883, 60)
    client.subscribe(SETTINGS.mosquitto_topic)

    print("Started listening")
    client.loop_forever()


if __name__ == "__main__":
    main()
