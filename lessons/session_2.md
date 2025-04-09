# Session 2

## Goals

- [x] Build a docker image for our `trades` service.
- [x] Deploy this image to our dev Kuberntes cluster
    - [x] Push the image to the docker registry
    - [x] Write a deployment.yaml file -> Kubernetes file
    - [x] Trigger the deployment with `kubectl apply -f ...` (manual deployment to start with)

- [x] Extract config parameters with pydantic-settings.

- [x] Automatic code linting and formatting with ruff and pre-commit.
    - [x] Install ruff and precommit using uv 
        ```sh
        # if you work outside the dev container you can install them as follows
        uv tool install ruff@latest
        uv tool install precommit@latest
        ```
    - [x] Set our precommit hooks
    - [x] Test it works.

- [ ] Start building the candles service, that aggregates trades into candles.

    - [x] Boilerplate code of a streaming app with Quixstreams.
    - [ ] Check these fake candles get to the output topic (Kafka UI)
    - [ ] Implement the actual transformation with quixstreams window functions.


## Challenges

- Rewrite the Dockerfile as a 2-stage build. If you manage to build an image with less than `300MB` you won (mine is `640MB`)

- Use secrets in the `trades.yaml` file instead of `env` parameters in the deployment. This is a bit of an overfkill here, but it is super
necessary when you want to pass things like API keys to your Python service.


