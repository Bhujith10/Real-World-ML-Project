# Runs the trades service as a standalone Pyton app (not Dockerized)
dev:
	uv run services/trades/src/trades/main.py

# Builds a docker image from a given Dockerfile
build:
	docker build -t trades:dev -f docker/trades.Dockerfile .

# Push the docker image to the docker registry of our kind cluster
push:
	kind load docker-image trades:dev --name rwml-34fa

# Deploys the docker image to the kind cluster
deploy: build push
	kubectl delete -f deployments/dev/trades/trades.yaml
	kubectl apply -f deployments/dev/trades/trades.yaml

lint:
	ruff check . --fix