# --- Config ---
COMPOSE_FILE := ./docker/docker-compose.yml
SERVICE      := flask-ml
CONTAINER    := ml-container

COMPOSE := docker compose -f $(COMPOSE_FILE)

# --- Commands ---
.PHONY: up build start stop restart logs exec pre-processing train down clean nuke

# start container detach and force the build
up:
	$(COMPOSE) up -d --build

# force build (with no cache, reinstall all dependencies), do not start container
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

pre-processing:
	@echo "Generate default values ..."
	docker exec -it $(CONTAINER) sh -lc 'export PYTHONPATH=/ml:$$PYTHONPATH && python app/command/generate_default_values.py'
	@echo "All default values were generated."

train:
	@echo "Start training Neural Network ..."
	docker exec -it $(CONTAINER) sh -lc 'export PYTHONPATH=/ml:$$PYTHONPATH && python app/command/train_neural_network_model.py'
	@echo "End training."

down:
	$(COMPOSE) down --remove-orphans

# Cleaning "safe" : Delete containers + project volumes
clean:
	$(COMPOSE) down --remove-orphans --volumes
