#include <project/certificate.h>

#include <Arduino.h>
#include <cstddef>
#include <cstdint>

extern const uint8_t
    CA_CERTIFICATE_start[] asm("_binary_data_certificate_pem_start");
extern const uint8_t
    CA_CERTIFICATE_end[] asm("_binary_data_certificate_pem_end");

void setupCertificate(WiFiClientSecure &client) {
    size_t dataSize = CA_CERTIFICATE_end - CA_CERTIFICATE_start;

    char caCertificate[dataSize + 1];
    memcpy(caCertificate, CA_CERTIFICATE_start, dataSize);
    caCertificate[dataSize] = '\0';

    client.setCACert(caCertificate);
}