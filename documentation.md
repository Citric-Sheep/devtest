# Elevator Demand Prediction System

This project models an elevator system and collects data that could be used to build a prediction engine for determining the optimal resting floor for elevators.

## Overview

When an elevator is empty and not moving, it is at its "resting floor". The ideal resting floor depends on the likely next floor that the elevator will be called from. This system collects data about elevator demands (when and where people call elevators) to enable future prediction of optimal resting floors.

## Key Concepts

- **Demand**: When people call an elevator from a specific floor, indicating their desired direction (up/down)
- **Resting Floor**: The floor where an elevator waits when it's vacant and not moving
- **Prediction**: Using historical demand data to determine the best floor for an elevator to rest on

## Project Structure

- `src/`: Source code directory
  - `models/`: Database models
  - `routes/`: API endpoints
  - `tests/`: Test files
- `alembic/`: Database migration files
- `Dockerfile`: Docker configuration
- `docker-compose.yml`: Docker Compose configuration

## Data Model

### Elevator

Represents an elevator in the system:
- `id`: Unique identifier
- `building_id`: Identifier for the building
- `max_floor`: Maximum floor the elevator can reach
- `min_floor`: Minimum floor the elevator can reach

### ElevatorDemand

Represents a demand for an elevator:
- `id`: Unique identifier
- `timestamp`: When the demand occurred
- `floor`: Which floor the demand came from
- `direction`: Whether the person wanted to go up or down
- `elevator_id`: Which elevator responded to this demand (optional)

## API Endpoints

### Elevators

- `POST /elevators/`: Register a new elevator
- `GET /elevators/`: List all elevators
- `GET /elevators/{id}`: Get elevator details
- `PUT /elevators/{id}`: Update an elevator
- `DELETE /elevators/{id}`: Delete an elevator

### Demands

- `POST /demands/`: Record a new elevator demand
- `GET /demands/`: List demands (with filtering options)

### Analytics

- `GET /demands/analytics/demand-by-floor`: Get demand frequency by floor
- `GET /demands/analytics/demand-by-hour`: Get demand frequency by hour and floor
- `GET /demands/analytics/direction-distribution`: Get up/down distribution by floor

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository
2. Run the application with Docker Compose:

```bash
docker-compose up -d
```

3. Access the API at http://localhost:8000
4. Access the API documentation at http://localhost:8000/docs

### Database Migrations

The project uses Alembic for database migrations:

```bash
# Inside the container
docker-compose exec api alembic revision --autogenerate -m "Initial migration"
docker-compose exec api alembic upgrade head
```

## Testing

Run the tests with:

```bash
docker-compose exec api -m pytest -v src/tests
```
