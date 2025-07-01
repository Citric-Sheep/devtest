#!/bin/bash

# Script to run the tests for the elevator demand prediction system in Docker.

# Build the containers if they don't exist
docker-compose build

# Run the tests
docker-compose run --rm api python -m pytest -v src/tests
