#include <project/connection.h>

#include <Arduino.h>

#include <project/config.h>

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

void connectToWifi(WiFiClientSecure &client, const char *ssid,
                   const char *password) {
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
    client.setCACert(CA_CERTIFICATE);
    Serial.println("[WiFi] CA certificate set.");
}

void connectToBroker(PubSubClient &client) {
    client.setServer(MOSQUITTO_HOST, MOSQUITTO_PORT);

    auto id = "ESP32 " + WiFi.macAddress();

    while (true) {
        Serial.print("[MQTT] Trying to connect as ");
        Serial.print(id);
        Serial.println('.');

        if (client.connect(id.c_str(), MOSQUITTO_USER, MOSQUITTO_PASSWORD)) {
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