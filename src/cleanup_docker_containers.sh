#!/bin/bash

docker-compose down --rmi all --remove-orphans || true
echo "May need to give password to remove database and migrations"
sudo rm -R data/
sudo rm -R evolvefg/netapp_endpoint/migrations/*