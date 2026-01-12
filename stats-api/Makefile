# COMPOSE is looking for a .env in his root directory ./docker

include .env

COMPOSE_FILE := ./docker/docker-compose.yml
SERVICE      := flask-stats
CONTAINER    := stats-container
DB_CONTAINER := database-container

# docker compose ... aim a service
COMPOSE := docker compose --env-file .env -f $(COMPOSE_FILE)

.PHONY: up build start stop restart logs exec down clean test lint fix-lint security-scan db-reset db-shell

up:
	$(COMPOSE) up -d --build

build:
	$(COMPOSE) build --no-cache

start:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) stop

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f $(SERVICE)

exec:
	docker exec -it $(CONTAINER) bash

down:
	$(COMPOSE) down --remove-orphans

clean:
	$(COMPOSE) down --remove-orphans --volumes

# docker exec ... aim a container
test:
	@echo "Running tests with pytest + coverage..."
	docker exec -it $(CONTAINER) sh -lc "export PYTHONPATH=/stats:$$PYTHONPATH && \
	coverage run -m pytest -q && coverage report -m"

lint:
	docker exec -it $(CONTAINER) sh -lc "flake8 /stats"

fix-lint:
	docker exec -it $(CONTAINER) sh -lc "autopep8 --in-place --aggressive --aggressive --recursive /stats"

security-scan:
	docker exec -it $(CONTAINER) sh -lc "safety check --full-report"

db-shell:
	docker exec -it $(DB_CONTAINER) mongosh -u ${MONGODB_ROOT_USER} -p ${MONGODB_ROOT_PASSWORD} --authenticationDatabase admin

db-reset:
	@echo "Suppression de la base ${MONGODB_DATABASE}..."
	docker exec -it $(DB_CONTAINER) mongosh -u ${MONGODB_ROOT_USER} -p ${MONGODB_ROOT_PASSWORD} --authenticationDatabase admin --eval "db.getSiblingDB('${MONGODB_DATABASE}').dropDatabase()"
	@echo "Création de la collection 'sales_madrid'..."
	docker exec -it $(DB_CONTAINER) mongosh -u ${MONGODB_ROOT_USER} -p ${MONGODB_ROOT_PASSWORD} --authenticationDatabase admin --eval "db.getSiblingDB('${MONGODB_DATABASE}').createCollection('sales_madrid')"
	@echo "Import du dataset..."
	docker exec -it $(CONTAINER) sh -lc "export PYTHONPATH=/stats:$$PYTHONPATH && python /stats/app/command/import_csv_to_mongodb.py"
