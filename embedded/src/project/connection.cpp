#include <project/connection.h>

#include <Arduino.h>

#include <project/config.h>

bool isWifiConnected() { return WiFi.status() == WL_CONNECTED; }

boolean tryToConnectToWifi(const char *ssid, const char *password) {
    for (int i = 0; i < 10; i++) {
        if (isWifiConnected()) {
            return true;
        }
        Serial.print(".");
        delay(1000);
    }
    return false;
}

bool connectToWifi(WiFiClientSecure &client, const char *ssid,
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
    client.setCACert(Config::CA_CERTIFICATE);
    Serial.println("[WiFi] CA certificate set.");

    return true;
}

void connectToBroker(PubSubClient &client) {
    client.setServer(Config::MOSQUITTO_HOST, Config::MOSQUITTO_PORT);

    auto id = Config::ESP_UNIQUE_ID;

    while (true) {
        Serial.print("[MQTT] Trying to connect as ");
        Serial.print(id);
        Serial.println('.');

        if (client.connect(id, Config::MOSQUITTO_USER,
                           Config::MOSQUITTO_PASSWORD)) {
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