#!/bin/bash

# Script to run the elevator demand prediction system in Docker.

# Build and start the containers
docker-compose up -d

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
sleep 5

# Apply migrations
echo "Applying migrations..."
docker-compose exec api python -m scripts.apply_migrations

# Initialize the database with sample data
echo "Initializing the database with sample data..."
docker-compose exec api python -m scripts.init_db

echo "The application is now running at http://localhost:8000"
echo "API documentation is available at http://localhost:8000/docs"
