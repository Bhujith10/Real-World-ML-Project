# Runs the trades service as a standalone Pyton app (not Dockerized)
dev:
	uv run services/${service}/src/${service}/main.py

# Builds and pushes the docker image to the given environment
build-and-push:
	./scripts/build-and-push-image.sh ${image_name} ${env}

# Deploys a service to the given environment
deploy:
	./scripts/deploy.sh ${service} ${env}

lint:
	ruff check . --fix

# Without this, we have to rename the consumer_group name everytime we restart the service
clean-state:
	rm -rf state/candles_consumer_group*