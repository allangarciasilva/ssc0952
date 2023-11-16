#include <Arduino.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <project/config.h>
#include <project/connection.h>
#include <project/mqtt.h>
#include <proto/NoiseMeasurement.pb.h>

const int soundPin = 35;

int cnt = 0;
float get_noise_voltage() {
    if (SIMULATION) {
        return cnt = (cnt + 1) % 30 + (cnt + 1) % 5;
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

WiFiClientSecure wifiClient;
PubSubClient client(wifiClient);

void setup() {
    Serial.begin(115200);
    pinMode(soundPin, INPUT);

    if (SIMULATION) {
        connectToWifi(wifiClient, "Wokwi-GUEST", "");
    } else {
        connectToWifi(wifiClient, Config::ESP_WIFI_SSID,
                      Config::ESP_WIFI_PASSWORD);
    }

    connectToBroker(client);

    Serial.println("Sending setup");
    client.publish("setup", "SETUP WENT OK");
}

void loop() {
    if (!client.connected()) {
        connectToBroker(client);
        return;
    }
    client.loop();

    NoiseMeasurement message = {0, 0, 0};
    message.room_id = 1;
    message.device_id = 1;

    float calculated_value = 0;

    int n = 10;
    for (int i = 0; i < n; i++) {
        calculated_value += get_noise_voltage();
        delay(50 / n);
    }

    calculated_value /= n;
    message.noise_value = calculated_value * calculated_value;

    if (publishMqttMessage(client, "default-topic", message)) {
        Serial.println(message.noise_value);
    } else {
        Serial.println("Error while sending message.");
    }
}