#!/bin/bash
docker-compose up --detach --remove-orphans --build
sleep 5
curl -s -o /dev/null --request GET http://localhost:8000/netappserver/api/v1/cells/update/