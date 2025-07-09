#!/bin/bash

# Kafka UI
echo "Forwarding Kafka UI..."
kubectl port-forward svc/kafka-ui 8080:8080 -n kafka &

# RisingWave SQL Frontend
echo "Forwarding RisingWave SQL Frontend..."
kubectl port-forward svc/risingwave-frontend 4567:4567 -n risingwave &

# RisingWave PostgreSQL
echo "Forwarding RisingWave PostgreSQL..."
kubectl port-forward svc/risingwave-postgresql 5432:5432 -n risingwave &

# Grafana Dashboard
echo "Forwarding Grafana..."

# MinIO
echo "Forwarding MinIO..."
kubectl port-forward svc/risingwave-minio 9000:9000 -n risingwave &
