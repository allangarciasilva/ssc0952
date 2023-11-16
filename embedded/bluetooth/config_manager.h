#pragma once

#include <proto/ESPConfig.pb.h>

#include <WiFiClientSecure.h>

class ConfigManager {
  public:
    static ConfigManager instance;
    void setData(uint8_t *buffer, size_t bufferSize);
    bool connectToWifi(WiFiClientSecure &client);

  private:
    ConfigManager();

    ESPConfig data = {"", ""};
    bool first_set = false;
    bool up_to_date = true;
};