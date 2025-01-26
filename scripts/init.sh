#!/bin/bash

# Start Minikube
if ! minikube status >/dev/null 2>&1; then
  echo "Starting Minikube..."
  minikube start
fi

# Load Docker image into Minikube
echo "Building Flask app image..."
docker build -t flask-app:latest .
minikube image load flask-app:latest

# Install PostgreSQL Helm Chart
echo "Installing PostgreSQL..."
helm install postgres k8s/postgres

# Install Flask App Helm Chart
echo "Installing Flask app..."
helm install flask-app k8s/flask-app

# Get services info
echo "Services running in Minikube:"
minikube service list