export VERSION ?= 3.0
DOCKERFILE = Dockerfile
DOCKER_COMPOSE = docker compose

default: run
clean: clean-dev
build: build-dev
run: run-dev
restart: stop-dev run-dev
fresh: clean-dev run-dev

stop-dev:
	$(DOCKER_COMPOSE) down --rmi all --remove-orphans || true

clean-dev: stop-dev
	@ echo "May need to give password to remove database and migrations"
	@ [ -d ./src/data ] && sudo rm -R ./src/data/ || :
	@ [ -f .env ] && sudo rm .env || :
	@ [ -d ./src/evolvefg/netapp_endpoint/migrations ] && sudo rm -R ./src/evolvefg/netapp_endpoint/migrations/* || :
	@ [ -d ./src/evolvefg/capif_onboarding ] && sudo rm ./src/evolvefg/capif_onboarding/* || :
	
build-dev: clean-dev

run-dev:
	@ cp env_to_copy.dev .env
	@ $(DOCKER_COMPOSE) up -d --remove-orphans --build
	@ sleep 10 && echo "Sleeping for 10s...."
	@ curl -s -o /dev/null -X GET 192.168.1.7:8000/netappserver/api/v1/cells/update/

guard-%:
        @ [ "${${*}}" = "" ] && echo "No $* detected" && exit 1 || :

.PHONY: default clean build run restart fresh