#!/bin/bash
# Steps:

# 1. Delete the cluster (if it exists, otherwise it will fail)
echo "Deleting the cluster..."
kind delete cluster --name rwml-34fa

# 2. Delete the docker network (if it exists, otherwise it will fail)
echo "Deleting the docker network..."
docker network rm rwml-34fa-network

# 3. Create the docker network
echo "Creating the docker network..."
docker network create --subnet 172.100.0.0/16 rwml-34fa-network

# 4. Create the cluster
echo "Creating the cluster..."
KIND_EXPERIMENTAL_DOCKER_NETWORK=rwml-34fa-network kind create cluster --config ./kind-with-portmapping.yaml

# 5. Install Kafka
echo "Installing Kafka..."
chmod +x ./install_kafka.sh
./install_kafka.sh

# 6. Install Kafka UI
echo "Installing Kafka UI..."
chmod +x ./install_kafka_ui.sh
./install_kafka_ui.sh

# 6. Install Kafka UI
echo "Installing Risingwave..."
chmod +x ./install_risingwave.sh
./install_risingwave.sh

# Kafka UI
echo "Forwarding Kafka UI..."
kubectl port-forward svc/kafka-ui 8080:8080 -n kafka &

# RisingWave SQL Frontend
echo "Forwarding RisingWave SQL Frontend..."
kubectl port-forward svc/risingwave 4567:4567 -n risingwave &

psql -h localhost -p 4567 -d dev -U root

echo "Forwarding RisingWave Minio..."
kubectl port-forward svc/risingwave-minio 9000:9000 9001:9001 -n risingwave &

# Go to risingwave minio, get accesskey and secretkey and paste in mlflow-minio-secret.yaml

kubectl create namespace mlflow
kubectl apply --recursive -f manifests/mlflow-minio-secret.yaml

# Run these commands to get username and password which would be asked when logging into mlflow in the browser
kubectl get secrets -n mlflow mlflow-tracking -o json | jq -r '.data."admin-password"' | base64 -d
kubectl get secrets -n mlflow mlflow-tracking -o json | jq -r '.data."admin-user"' | base64 -d

# To use mlflow
# Open a shell inside the risingwave-postgresql-0 pod
kubectl exec -it risingwave-postgresql-0 -n risingwave -- bash
# Access the p-sql shell inside the pod
psql -U postgres -h risingwave-postgresql.risingwave.svc.cluster.local
# when prompted for password enter
postgres
# inside psql shell
CREATE USER mlflow WITH ENCRYPTED PASSWORD 'mlflow';
CREATE DATABASE mlflow WITH ENCODING='UTF8' OWNER=mlflow;
CREATE DATABASE mlflow_auth WITH ENCODING='UTF8' OWNER=mlflow;
# exit the pod shell
exit

helm upgrade --install --create-namespace --wait mlflow oci://registry-1.docker.io/bitnamicharts/mlflow --namespace=mlflow --values deployments/dev/kind/manifests/mlflow-values.yaml

kubectl -n mlflow port-forward svc/mlflow-tracking 8889:80




