install:
	docker compose -f ./docker/docker-compose.yml up -d --build
.PHONY: install

start:
	docker exec -it psid-api-container flask run --port 8000
.PHONY: install

exec:
	docker exec -it psid-api-container bash
.PHONY: exec

test:
	@echo "Lancement des tests..."
	docker exec psid-api-container sh -c "export PYTHONPATH=/psid/app:$$PYTHONPATH && \
	coverage run --omit='app/test/*' -m unittest discover && \
	coverage xml && \
	coverage report -m"
.PHONY: test


lint:
	docker exec -it psid-api-container flake8 .
.PHONY: lint

fix-lint:
	docker exec -it psid-api-container autopep8 --in-place --aggressive --aggressive --recursive .
.PHONY: lint

security-scan:
	docker exec -it psid-api-container safety check --full-report
.PHONY: security-scan

db-reset:
	@echo "Suppression de la base de données ..."
	docker exec database-container mongosh -u admin -p ChangeMe --authenticationDatabase admin --eval "db.dropDatabase()" sales
	@echo "Création de la collection 'sales_madrid' dans la base de données..."
	docker exec database-container mongosh -u admin -p ChangeMe --authenticationDatabase admin --eval "db.createCollection('sales_madrid')" sales
	@echo "Import du dataset ..."
	docker exec psid-api-container sh -c 'export PYTHONPATH=/psid/app:$$PYTHONPATH && python app/command/import_csv_to_mongodb.py'
.PHONY: db-reset

kill:
	docker system prune -a
	docker kill psid-api-container database-container
	docker rm psid-api-container database-container
	docker images
.PHONY: kill


