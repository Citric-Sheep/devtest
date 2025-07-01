@echo off
REM Script to run the tests for the elevator demand prediction system in Docker on Windows.

REM Build the containers if they don't exist
echo Building containers...
docker-compose build --no-cache

REM Run the tests
echo Running tests...
docker-compose run --rm api python -m pytest -v src/tests
