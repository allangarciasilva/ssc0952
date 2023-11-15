#include <Arduino.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <pb_common.h>
#include <pb_encode.h>
#include <project/config.h>
#include <project/connection.h>
#include <project/mqtt.h>
#include <proto/NoiseMeasurement.pb.h>

#define SIMULATION 1

WiFiClientSecure wifiClient;
PubSubClient client(wifiClient);

const int soundPin = 35;

float get_noise_voltage() {
    if (SIMULATION) {
        return 9.0;
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

void setup() {
    Serial.begin(115200);
    pinMode(soundPin, INPUT);

    if (SIMULATION) {
        connectToWifi(wifiClient, "Wokwi-GUEST", "");
    } else {
        connectToWifi(wifiClient, ESP_WIFI_SSID, ESP_WIFI_PASSWORD);
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
    message.noise_value = get_noise_voltage();

    if (publishMqttMessage(client, "default-topic", message)) {
        Serial.println(message.noise_value);
    } else {
        Serial.println("Error while sending message.");
    }

    delay(1000);
}