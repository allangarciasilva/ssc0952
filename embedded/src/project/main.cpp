#include <Arduino.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <pb_common.h>
#include <pb_encode.h>
#include <project/certificate.h>
#include <project/mqtt.h>
#include <proto/NoiseMeasurement.pb.h>

#define SIMULATION 0

WiFiClientSecure wifiClient;
PubSubClient client(wifiClient);

boolean tryToConnectToWifi(const char *ssid, const char *password) {
    for (int i = 0; i < 10; i++) {
        if (WiFi.status() == WL_CONNECTED) {
            return true;
        }
        Serial.print(".");
        delay(1000);
    }
    return false;
}

void connectToWifi(const char *ssid, const char *password) {
    while (true) {
        Serial.print("[WiFi] Trying to connect to ");
        Serial.print(ssid);
        Serial.print('.');

        WiFi.mode(WIFI_STA); // Optional
        WiFi.begin(ssid, password);

        if (tryToConnectToWifi(ssid, password)) {
            break;
        }

        Serial.print("\n[WiFi] Error while connecting to ");
        Serial.print(ssid);
        Serial.println(". Trying again in 5 seconds.");
        delay(5000);
    }

    Serial.print("\n[WiFi] Connected to ");
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
        Serial.print(id);
        Serial.print(". Error code: ");
        Serial.print(client.state());
        Serial.println(". Trying again in 5 seconds.");
        delay(5000);
    }

    Serial.print("[MQTT] Connected as ");
    Serial.print(id);
    Serial.println('.');
}

IPAddress mqttHost(143, 107, 232, 252);
int mqttPort = 7045;
const char *mqttUser = "ssc0952";
const char *mqttPassword = "MEbj5DgYosYVYyzNyLKI/5R2XIUmfC6LZheGJQWGXb0=";

const int soundPin = 35;

void setup() {
    Serial.begin(115200);
    pinMode(soundPin, INPUT);

    // connectToWifi("Allan's Galaxy S20 FE 5G", "12345678");
    if (SIMULATION) {
        connectToWifi("Wokwi-GUEST", "");
    } else {
        connectToWifi("2G_APT31", "banana11");
    }

    delay(2000);

    connectToBroker(mqttHost, mqttPort, mqttUser, mqttPassword);

    Serial.println("Sending setup");
    client.publish("setup", "SETUP WENT OK");
}

int cnt = 0;

float get_noise_voltage() {
    if (SIMULATION) {
        return cnt;
    }
    float minim = analogRead(soundPin);
    float curr;
    for (int i = 0; i < 10; i++) {
        curr = analogRead(soundPin);
        minim = minim < curr ? minim : curr;
    }
    minim *= (5.0 / 1023.0);
    return minim;
}

void loop() {
    if (!client.connected()) {
        connectToBroker(mqttHost, mqttPort, mqttUser, mqttPassword);
        return;
    }
    client.loop();

    NoiseMeasurement message = {0, 0, 0};
    message.room_id = 1;
    message.device_id = 2;
    message.noise_value = get_noise_voltage();
    cnt++;

    if (publishMqttMessage(client, "default-topic", message)) {
        // Serial.print(cnt);
        // Serial.print(" -> Sent message: ");
        Serial.println(message.noise_value);
    } else {
        // Serial.println("Error while sending message.");
    }

    delay(100);
}