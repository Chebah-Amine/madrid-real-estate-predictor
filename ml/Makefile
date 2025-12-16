install:
	docker compose -f ./docker/docker-compose.yml up -d --build
.PHONY: install

start:
	docker exec -it psid-ml-container flask run --port 7000
.PHONY: install

exec:
	docker exec -it psid-ml-container bash
.PHONY: exec

pre-processing:
	@echo "Generate default values ..."
	docker exec psid-ml-container sh -c 'export PYTHONPATH=/psid/app:$$PYTHONPATH && \
	python app/command/generate_default_values.py'
	@echo "All default values were generated ..."
.PHONY: pre-processing

train:
	@echo "Start training Neural Network ..."
	docker exec psid-ml-container sh -c 'export PYTHONPATH=/psid/app:$$PYTHONPATH && \
	python app/command/train_neural_network_model.py'
	@echo "End training Neural Network ..."
.PHONY: train

kill:
	docker system prune -a
	docker kill psid-ml-container
	docker rm psid-ml-container
	docker images
.PHONY: kill


