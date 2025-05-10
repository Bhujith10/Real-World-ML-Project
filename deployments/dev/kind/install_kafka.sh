kubectl create namespace kafka
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Wait for Strimzi operator pod to be ready
echo "Waiting for Strimzi operator to be ready..."
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=120s

kubectl apply -f manifests/kafka-e11b.yaml