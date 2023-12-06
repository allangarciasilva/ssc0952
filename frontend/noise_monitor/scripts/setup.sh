#!/bin/bash

rm -rf .env proto
cp ../../proto proto -r

GEN_FILE=$PWD/lib/gen/api_host.dart
mkdir -p $(dirname $GEN_FILE)

source $PWD/../../config.env
echo "const String API_HOST = \"$API_HOST\";" > $GEN_FILE
echo "const int HTTP_PORT = $HTTP_PORT;" >> $GEN_FILE
echo "const int WS_PORT = $WS_PORT;" >> $GEN_FILE