#!/bin/bash

GEN_FILE=$PWD/lib/gen/api_host.dart
mkdir -p $(dirname $GEN_FILE)

echo source $PWD/.env
echo "const String API_HOST = \"143.107.232.252\";" > $GEN_FILE
echo "const int API_PORT = 8045;" >> $GEN_FILE

mkdir -p ./proto
cp -u ../proto/*.proto ./proto