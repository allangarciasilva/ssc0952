#!/bin/bash

SCRIPTS_DIR=$(dirname "$0")
ROOT_DIR=$(realpath "$SCRIPTS_DIR/..")
KUBERNETES_DIR="$ROOT_DIR/kubernetes"

set -o allexport
source "$ROOT_DIR/../config.env"
set +o allexport

mkdir -p "$KUBERNETES_DIR/replaced/"

for filepath in $KUBERNETES_DIR/templates/*.yaml; do
  filename=$(basename "$filepath")
  envsubst < "$filepath" > "$KUBERNETES_DIR/replaced/$filename"
done
