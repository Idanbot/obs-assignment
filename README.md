# Weather Service

A Flask-based weather service application that integrates with PostgreSQL and is designed for deployment on Kubernetes. The application fetches weather data for random cities using the Open-Meteo API and stores the data in a PostgreSQL database for analysis.

---

## Features

- Fetches weather data for the past 30 days for random cities.
- Stores data in PostgreSQL for future analysis.
- Offers endpoints for querying weather data for specific cities.
- Supports deployment using Kubernetes (Minikube or AKS).

---

## Prerequisites

Before running the service, ensure the following tools are installed and configured:

1. **Kubernetes**:
   - For local testing, install [Minikube](https://minikube.sigs.k8s.io/docs/start/).
   - For cloud deployment, set up an AKS cluster. [Learn more](https://learn.microsoft.com/en-us/azure/aks/).
2. **Helm**: Package manager for Kubernetes. [Install Helm](https://helm.sh/docs/intro/install/).

---

## Setup Instructions

### ** Running Locally**
#### Using Docker Compose
Navigate to the project root and run the following command:
```bash
docker-compose up
```

#### Using `scripts/init.sh`
Navigate to the `scripts` folder and run `init.sh` to set up the project:
```bash
cd scripts
chmod +x init.sh
sudo ./init.sh
```

## Endpoints
### 1. **Random Weather**
Fetch weather data for a random city.
GET `/weather/random`

### 2. **Last 30 Days**
Fetch weather data for the past 30 days for a specific city.
GET `/weather/city/<city_name>`

### 3. **Health Check**
Verify that the service is running.
GET `/health`