#!/bin/bash

sh ../compile_protobuf.sh

set -a
source $PWD/.env
set +a

python3 ./scripts/_setup_consts.py