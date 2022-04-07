#!/bin/bash
docker-compose up --detach --remove-orphans --build

cd pygui
docker build -t pygui .