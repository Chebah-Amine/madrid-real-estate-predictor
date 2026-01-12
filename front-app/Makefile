# ---- Config ----
COMPOSE_FILE := ./docker/docker-compose.yml
SERVICE      := front-web
CONTAINER    := front-container

COMPOSE := docker compose -f $(COMPOSE_FILE)

# ---- Default ----
.PHONY: help
help:
	@echo "Targets:"
	@echo "  up        - Build & start the Angular dev container (detached)"
	@echo "  start     - Start container (no build)"
	@echo "  build     - Rebuild image (no cache)"
	@echo "  stop      - Stop containers"
	@echo "  down      - Stop & remove containers"
	@echo "  clean     - Down + remove volumes (node_modules cache inside volume)"
	@echo "  logs      - Follow logs"
	@echo "  exec      - Shell into container"
	@echo "  install   - Install npm dependencies inside container (npm ci)"
	@echo "  ng        - Run Angular CLI command (usage: make ng ARGS='build')"
	@echo "  test      - Run unit tests"
	@echo "  lint      - Run lint"
	@echo "  format    - Run formatter if configured (prettier)"
	@echo "  status    - Show compose status"

# ---- Lifecycle ----
.PHONY: up
up:
	$(COMPOSE) up -d --build

.PHONY: start
start:
	$(COMPOSE) up -d

.PHONY: build
build:
	$(COMPOSE) build --no-cache

.PHONY: stop
stop:
	$(COMPOSE) stop

.PHONY: down
down:
	$(COMPOSE) down --remove-orphans

.PHONY: clean
clean:
	$(COMPOSE) down --remove-orphans --volumes

.PHONY: status
status:
	$(COMPOSE) ps

# ---- Logs / Exec ----
.PHONY: logs
logs:
	$(COMPOSE) logs -f $(SERVICE)

.PHONY: exec
exec:
	docker exec -it $(CONTAINER) sh

# ---- NPM / Angular CLI ----
.PHONY: install
install:
	# Ensure container is up so node_modules volume exists
	$(COMPOSE) up -d $(SERVICE)
	docker exec -it $(CONTAINER) sh -lc "npm ci"

# Run any Angular CLI command via ARGS
# Example: make ng ARGS="update @angular/core @angular/cli"
.PHONY: ng
ng:
	@if [ -z "$(ARGS)" ]; then \
		echo "Usage: make ng ARGS='...'; Example: make ng ARGS='build'"; \
		exit 1; \
	fi
	docker exec -it $(CONTAINER) sh -lc "npx ng $(ARGS)"

# ---- Quality ----
.PHONY: test
test:
	docker exec -it $(CONTAINER) sh -lc "npm test -- --watch=false"

.PHONY: lint
lint:
	docker exec -it $(CONTAINER) sh -lc "npm run lint"

.PHONY: format
format:
	# Only works if you have a 'format' script in package.json
	docker exec -it $(CONTAINER) sh -lc "npm run format"
