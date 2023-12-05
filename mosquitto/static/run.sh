#!/bin/sh

PASSWORD_FILE=/mosquitto/password/password_file
OPENSSL_CONFIG_FILE=/mosquitto/openssl.cnf
CERT_PATH=/mosquitto/certs

# Criação dos certificados SSL

echo "Generating SSL certificates..."

if [ ! -f "$CERT_PATH/ca.crt" ]; then
    mkdir -p "$CERT_PATH"
    openssl genrsa -out $CERT_PATH/ca.key 2048
    openssl req -new -x509 -days 1826 -key $CERT_PATH/ca.key -out $CERT_PATH/ca.crt -config $OPENSSL_CONFIG_FILE
    openssl genrsa -out $CERT_PATH/server.key 2048
    openssl req -new -out $CERT_PATH/server.csr -key $CERT_PATH/server.key -config $OPENSSL_CONFIG_FILE
    openssl x509 -req -in $CERT_PATH/server.csr -CA $CERT_PATH/ca.crt -CAkey $CERT_PATH/ca.key -CAcreateserial -out $CERT_PATH/server.crt -days 360
    echo "Done"
else
    echo "Found SSL certificates, skipping."
fi

# Criação do arquivo de senhas, utilizando as variáveis $MOSQUITTO_USER e $MOSQUITTO_PASSWORD.

echo "Setting up user..."

rm -rf "$PASSWORD_FILE" && mkdir -p $(dirname "$PASSWORD_FILE") && touch "$PASSWORD_FILE"
chown mosquitto "$PASSWORD_FILE"
chgrp mosquitto "$PASSWORD_FILE"
chmod 0700 "$PASSWORD_FILE"
mosquitto_passwd -H sha512 -b "$PASSWORD_FILE" "$MOSQUITTO_USER" "$MOSQUITTO_PASSWORD"
echo "Done"

# Executa o processo principal

/usr/sbin/mosquitto -c /mosquitto/config/mosquitto.conf
