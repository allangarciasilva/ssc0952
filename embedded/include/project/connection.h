#pragma once

#include <PubSubClient.h>
#include <WiFiClientSecure.h>

void connectToWifi(WiFiClientSecure &client, const char *ssid,
                   const char *password);
void connectToBroker(PubSubClient &client);