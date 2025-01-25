# Use Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app/ ./app

# Expose the application port
EXPOSE 8080

# Set environment variable for Flask to run
ENV FLASK_APP=app/main.py

# Start the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]