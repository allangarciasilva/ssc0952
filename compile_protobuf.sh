ROOT_PATH=$(dirname $(realpath "$0"))
PROTO_FILES=$ROOT_PATH/proto/*.proto

echo "Installing protoc"
python3 -m pip install grpcio-tools > /dev/null

echo "Setting up directories"
PY_OUT_MODULE=$ROOT_PATH/backend/proto
ESP_OUTPUT_INCLUDE=$ROOT_PATH/embedded/include/proto
ESP_OUTPUT_SRC=$ROOT_PATH/embedded/src/generated
rm -rf $PY_OUT_MODULE $ESP_OUTPUT_INCLUDE $ESP_OUTPUT_SRC
mkdir -p $PY_OUT_MODULE $ESP_OUTPUT_INCLUDE $ESP_OUTPUT_SRC

echo "Building for Python"
touch $PY_OUT_MODULE/__init__.py
python3 -m grpc.tools.protoc $PROTO_FILES -I $ROOT_PATH --python_out=$PY_OUT_MODULE/.. --pyi_out=$PY_OUT_MODULE/.. 2> /dev/null

echo "Building for ESP32"
python3 -m grpc.tools.protoc $PROTO_FILES -I $ROOT_PATH --nanopb_out=$ESP_OUTPUT_INCLUDE/.. 2> /dev/null
mv $ESP_OUTPUT_INCLUDE/*.c $ESP_OUTPUT_SRC