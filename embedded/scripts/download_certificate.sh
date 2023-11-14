#!/bin/bash

mkdir -p data

openssl s_client \
    -connect andromeda.lasdpc.icmc.usp.br:7045 \
    -showcerts </dev/null | openssl x509 -outform PEM > data/certificate.pem

CERTIFICATE=$(cat ./data/certificate.pem)
CERTIFICATE_CPP_FILE=./src/generated/certificate.cpp

echo "#include <project/certificate.h>" > $CERTIFICATE_CPP_FILE
echo "const char *CA_CERTIFICATE = R\"(" >> $CERTIFICATE_CPP_FILE
echo "$CERTIFICATE" >> $CERTIFICATE_CPP_FILE
echo ")\";" >> $CERTIFICATE_CPP_FILE;