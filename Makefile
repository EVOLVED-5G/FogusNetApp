export VERSION ?= 3.0
DOCKERFILE = Dockerfile
DOCKER_COMPOSE = docker compose

default: build
build: build-dev
clean: clean-dev
run: run-dev

clean-dev:
	
build-dev: clean-dev


run-dev:
	@ [ -f .env ] && docker ps | grep netapp > /dev/null && $(DOCKER_COMPOSE) stop || echo "Skipping $(DOCKER_COMPOSE) stop"
	@ [ -f ./src/data ] && ./cleanup_docker_containers.sh || :
	@ cp env_to_copy.dev .env
	@ $(DOCKER_COMPOSE) up -d --remove-orphans --build
	@ sleep 10 && echo "Sleeping for 10s...."
	@ curl -X GET 192.168.1.4:8000/netappserver/api/v1/cells/update/

guard-%:
        @ [ "${${*}}" = "" ] && echo "No $* detected" && exit 1 || :

.PHONY: clean-dev build-dev