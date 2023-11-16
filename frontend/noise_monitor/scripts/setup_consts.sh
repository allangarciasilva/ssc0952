#!/bin/bash

SCRIPT_PATH=$(dirname $(realpath "$0"))
FRONTEND_PATH=$(realpath $SCRIPT_PATH/..)
ROOT_PATH=$(realpath $FRONTEND_PATH/../..)

PROTO_FILES=$ROOT_PATH/proto/*.proto

FLUTTER_OUTPUT_DIR=$FRONTEND_PATH/lib/proto
rm -rf $FLUTTER_OUTPUT_DIR
mkdir -p $FLUTTER_OUTPUT_DIR

echo "Building Protobuf"
cd $FRONTEND_PATH/ > /dev/null
flutter pub add protobuf > /dev/null
dart pub global activate protoc_plugin > /dev/null
export PATH="$PATH":"$HOME/.pub-cache/bin"
protoc $PROTO_FILES -I $ROOT_PATH --dart_out=$FLUTTER_OUTPUT_DIR/.. > /dev/null