ROOT_PATH=$(dirname $(realpath "$0"))
PROTO_FILES=$ROOT_PATH/proto/*.proto

echo "Installing protoc"
python3 -m pip install grpcio-tools > /dev/null

echo "Setting up directories"
PY_OUT_MODULE=$ROOT_PATH/backend/proto
rm -rf $PY_OUT_MODULE
mkdir -p $PY_OUT_MODULE

echo "Building for Python"
touch $PY_OUT_MODULE/__init__.py
python3 -m grpc.tools.protoc $PROTO_FILES -I $ROOT_PATH --python_out=$PY_OUT_MODULE/.. --pyi_out=$PY_OUT_MODULE/.. 2> /dev/null