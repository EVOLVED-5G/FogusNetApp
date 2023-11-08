#!/bin/bash

docker-compose down --rmi all --remove-orphans || true
echo "May need to give password to remove database and migrations"
sudo rm -R ./src/data/
sudo rm .env
sudo rm -R ./src/evolvefg/netapp_endpoint/migrations/*
sudo rm ./src/evolvefg/capif_onboarding/*