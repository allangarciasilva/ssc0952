#pragma once

#include <IPAddress.h>

namespace Config {

extern const char *CA_CERTIFICATE;

extern const char *ESP_UNIQUE_ID;
extern const char *ESP_WIFI_SSID;
extern const char *ESP_WIFI_PASSWORD;

extern const char *MOSQUITTO_USER;
extern const char *MOSQUITTO_PASSWORD;
extern IPAddress MOSQUITTO_HOST;
extern int MOSQUITTO_PORT;

} // namespace Config