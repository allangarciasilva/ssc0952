#!/bin/bash

EMBEDDED_PATH="$PWD"

cd ..
sh ./compile_protobuf.sh

cd "$EMBEDDED_PATH"
set -a
source $EMBEDDED_PATH/.env
set +a

python3 ./scripts/_setup_consts.py