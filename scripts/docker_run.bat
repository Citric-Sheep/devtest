@echo off
REM Script to run the elevator demand prediction system in Docker on Windows.

REM Build and start the containers
echo Building and starting containers...
docker-compose up -d

REM Wait for the database to be ready
echo Waiting for the database to be ready...
timeout /t 5 /nobreak > nul

REM Apply migrations
echo Applying migrations...
docker-compose exec api python -m scripts.apply_migrations

REM Initialize the database with sample data
echo Initializing the database with sample data...
docker-compose exec api python -m scripts.init_db

echo.
echo The application is now running at http://localhost:8000
echo API documentation is available at http://localhost:8000/docs
