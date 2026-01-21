include ./stats-api/.env

COMPOSE_FILE := ./docker-compose.yml
COMPOSE := docker compose --env-file ./stats-api/.env -f $(COMPOSE_FILE)
DB_CONTAINER := database-container

.PHONY: up start stop down clean logs ps rebuild exec-ml exec-stats exec-front

up:
	$(COMPOSE) up -d --build

start:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) stop

down:
	$(COMPOSE) down --remove-orphans

clean:
	$(COMPOSE) down --remove-orphans --volumes

rebuild:
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

cnt ?=
exec:
	docker exec -it $(cnt) bash

db-shell:
	docker exec -it $(DB_CONTAINER) mongosh -u ${MONGODB_ROOT_USER} -p ${MONGODB_ROOT_PASSWORD} --authenticationDatabase admin

svc ?=
logs:
	$(COMPOSE) logs -f $(svc)
