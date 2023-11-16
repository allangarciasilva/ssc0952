#include <project/config_manager.h>

#include <Arduino.h>
#include <pb_common.h>
#include <pb_decode.h>

#include <project/connection.h>

ConfigManager ConfigManager::instance;

ConfigManager::ConfigManager() {}

void ConfigManager::setData(uint8_t *buffer, size_t bufferSize) {
    pb_istream_t stream = pb_istream_from_buffer(buffer, bufferSize);
    if (!pb_decode(&stream, ESPConfig_fields, &data)) {
        Serial.println("Error while decoding config from BLE.");
    }

    first_set = true;
    up_to_date = false;

    Serial.println("Configuration set!");
}

bool ConfigManager::connectToWifi(WiFiClientSecure &client) {
    if (!first_set) {
        Serial.println("Missing configuration.");
        return false;
    }

    if (up_to_date && isWifiConnected()) {
        return true;
    }

    return ::connectToWifi(client, data.wifiSsid, data.wifiPassword);
}