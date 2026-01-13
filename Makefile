COMPOSE_FILE := ./docker-compose.yml
COMPOSE := docker compose --env-file ./stats-api/.env -f $(COMPOSE_FILE)

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

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

rebuild:
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

exec-ml:
	docker exec -it ml-container sh

exec-stats:
	docker exec -it stats-container sh

exec-front:
	docker exec -it front-container sh
