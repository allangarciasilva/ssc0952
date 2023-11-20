#!/bin/bash

echo "Building Protobuf"
mkdir -p ./include/proto ./src/proto
protoc ./proto/*.proto -I. --nanopb_out=./include
mv ./include/proto/*.c ./src/proto/

echo "Building constants"
python3 ./scripts/_setup_consts.py