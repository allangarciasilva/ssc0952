ROOT_PATH=$(dirname $(realpath "$0"))
PROTO_FILES=$ROOT_PATH/proto/*.proto

echo "Installing protoc"
python3 -m pip install grpcio-tools nanopb > /dev/null

echo "Setting up directories"
PY_OUT_MODULE=$ROOT_PATH/backend/proto
ESP_OUTPUT_INCLUDE=$ROOT_PATH/embedded/include/proto
ESP_OUTPUT_SRC=$ROOT_PATH/embedded/src/generated
FLUTTER_OUTPUT_DIR=$ROOT_PATH/frontend/noise_monitor/lib/proto
rm -rf $PY_OUT_MODULE $ESP_OUTPUT_INCLUDE $ESP_OUTPUT_SRC $FLUTTER_OUTPUT_DIR
mkdir -p $PY_OUT_MODULE $ESP_OUTPUT_INCLUDE $ESP_OUTPUT_SRC $FLUTTER_OUTPUT_DIR

echo "Building for Python"
touch $PY_OUT_MODULE/__init__.py
python3 -m grpc.tools.protoc $PROTO_FILES -I $ROOT_PATH --python_out=$PY_OUT_MODULE/.. --pyi_out=$PY_OUT_MODULE/.. 2> /dev/null

echo "Building for ESP32"
python3 -m grpc.tools.protoc $PROTO_FILES -I $ROOT_PATH --nanopb_out=$ESP_OUTPUT_INCLUDE/..
mv $ESP_OUTPUT_INCLUDE/*.c $ESP_OUTPUT_SRC

echo "Building for Flutter"
cd $ROOT_PATH/frontend/noise_monitor/ > /dev/null
flutter pub add protobuf > /dev/null
dart pub global activate protoc_plugin > /dev/null
export PATH="$PATH":"$HOME/.pub-cache/bin"
protoc $PROTO_FILES -I $ROOT_PATH --dart_out=$FLUTTER_OUTPUT_DIR/.. > /dev/null