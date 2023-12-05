#!/bin/bash

DOCKER_USER="allangarcia2004"
DOCKER_IMAGE=$DOCKER_USER/ssc0965

docker build -t $DOCKER_IMAGE . && \
docker push $DOCKER_IMAGE