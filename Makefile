# Runs the trades service as a standalone Pyton app (not Dockerized)
dev:
	uv run services/$(service)/src/$(service)/main.py

# Builds a docker image from a given Dockerfile
build:
	docker build -t $(service):dev -f docker/$(service).Dockerfile .

# Push the docker image to the docker registry of our kind cluster
push:
	kind load docker-image $(service):dev --name rwml-34fa

# Deploys the docker image to the kind cluster
deploy: build push
	kubectl delete -f deployments/dev/$(service).yaml --ignore-not-found=true
	kubectl apply -f deployments/dev/$(service).yaml

lint:
	ruff check . --fix