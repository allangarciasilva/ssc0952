#include <Arduino.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <pb_common.h>
#include <pb_encode.h>
#include <project/certificate.h>
#include <project/mqtt.h>
#include <proto/NoiseMeasurement.pb.h>

WiFiClientSecure wifiClient;
PubSubClient client(wifiClient);

void connectToWifi(const char *ssid, const char *password) {
    while (true) {
        Serial.print("[WiFi] Trying to connect to ");
        Serial.print(ssid);
        Serial.println('.');

        WiFi.begin(ssid, password, 6);
        if (WiFi.status() == WL_DISCONNECTED) {
            break;
        }

        Serial.print("[WiFi] Error while connecting to ");
        Serial.print(ssid);
        Serial.println(". Trying again in 5 seconds.");
        delay(5000);
    }

    Serial.print("[WiFi] Connected to ");
    Serial.print(ssid);
    Serial.println('.');

    Serial.println("[WiFi] Setting up CA certificate.");
    wifiClient.setCACert(CA_CERTIFICATE);
    Serial.println("[WiFi] CA certificate set.");
}

template <typename Host>
void connectToBroker(Host host, int port, const char *username,
                     const char *password) {
    client.setServer(host, port);

    auto id = "ESP32 " + WiFi.macAddress();

    while (true) {
        Serial.print("[MQTT] Trying to connect as ");
        Serial.print(id);
        Serial.println('.');

        if (client.connect(id.c_str(), username, password)) {
            break;
        }

        Serial.print("[MQTT] Error while connecting as ");
        Serial.print(". Error code: ");
        Serial.print(client.state());
        Serial.println(". Trying again in 5 seconds.");
        delay(5000);
    }

    Serial.print("[MQTT] Connected as ");
    Serial.print(id);
    Serial.println('.');
}

const char *mqttHost = "andromeda.lasdpc.icmc.usp.br";
int mqttPort = 7045;
const char *mqttUser = "ssc0952";
const char *mqttPassword = "MEbj5DgYosYVYyzNyLKI/5R2XIUmfC6LZheGJQWGXb0=";

void setup() {
    Serial.begin(115200);

    connectToWifi("Wokwi-GUEST", "");

    delay(2000);

    connectToBroker(mqttHost, mqttPort, mqttUser, mqttPassword);

    Serial.println("Sending setup");
    client.publish("setup", "SETUP WENT OK");
}

int cnt = 0;

void loop() {
    if (!client.connected()) {
        Serial.println("Pau");
        connectToBroker(mqttHost, mqttPort, mqttUser, mqttPassword);
        return;
    }
    client.loop();

    int sign = cnt % 2 == 0 ? -1 : 1;

    NoiseMeasurement message = {0, 0, 0};
    message.room_id = cnt;
    message.device_id = cnt * 2;
    message.noise_value = cnt * sign * 3;
    cnt++;

    if (publishMqttMessage(client, "default-topic", message)) {
        Serial.print(cnt);
        Serial.println(" -> Sent message.");
    } else {
        Serial.println("Error while sending message.");
    }

    delay(500);
}