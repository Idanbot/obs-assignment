# TODO - Add a description of the project

# Setup
Inside scripts folder, run init.sh to install dependencies and setup the project.
remember to give permission to the script to run.
```bash
chmod +x scripts/start-minikube.sh
```

# Docker
```bash
docker build -t weather-service .
docker run -p 8080:8080 weather-service
```

# Docker Compose
```bash
docker-compose up --build
docker-compose down -v
```