#!/bin/bash

if [ -z "$1" ]
  then
    echo "No NetApp IP given"
    echo "e.g. ./run_only_gui.sh localhost"
    exit 0
fi

curl -s -o /dev/null --request GET http://$1:8000/netappserver/api/v1/cells/update/ | jq

cd pygui
docker build -t pygui .
docker run --network=host -u=$(id -u $USER):$(id -g $USER) -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v $(pwd)/app:/app --rm pygui