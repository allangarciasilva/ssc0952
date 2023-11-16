#!/bin/bash

SCRIPT_PATH=$(dirname $(realpath "$0"))
EMBEDDED_PATH=$(realpath $SCRIPT_PATH/..)
ROOT_PATH=$(realpath $EMBEDDED_PATH/..)

PROTO_FILES=$ROOT_PATH/proto/*.proto

ESP_OUTPUT_INCLUDE=$EMBEDDED_PATH/include/proto
ESP_OUTPUT_SRC=$EMBEDDED_PATH/src/generated
rm -rf $ESP_OUTPUT_INCLUDE $ESP_OUTPUT_SRC
mkdir -p $ESP_OUTPUT_INCLUDE $ESP_OUTPUT_SRC

echo "Building Protobuf"
python3 -m pip install grpcio-tools nanopb > /dev/null
python3 -m grpc.tools.protoc $PROTO_FILES -I $ROOT_PATH --nanopb_out=$ESP_OUTPUT_INCLUDE/.. 2> /dev/null
mv $ESP_OUTPUT_INCLUDE/*.c $ESP_OUTPUT_SRC

set -a
source $EMBEDDED_PATH/.env
set +a

echo "Building constants"
cd $EMBEDDED_PATH
python3 ./scripts/_setup_consts.py