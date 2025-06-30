# Elevator Prediction System

A focused system for collecting elevator data to train ML models that predict optimal resting floors.

## Overview

This system implements the **"Golden Event"** approach for elevator prediction:
- **Core Concept**: When an elevator is resting on floor X at time T, and the next call comes from floor Y
- **ML Goal**: Predict the most likely call floor based on current resting floor and time
- **Data Design**: Single table capturing the critical resting→call relationship

## The Golden Event

The system focuses on capturing the most important data point for ML prediction:

```
Elevator resting on floor X at time T → Next call from floor Y
```

This relationship is logged in the `demand_log` table with all the features needed for ML training.

## Database Schema

### DemandLog Table (Single Table Design)

| Column | Type | ML Purpose |
|--------|------|------------|
| id | Integer | Primary key |
| timestamp_rested | DateTime | **Feature**: When elevator became idle |
| timestamp_called | DateTime | **Feature**: When next call was received |
| resting_floor | Integer | **Feature**: Floor elevator was resting on |
| call_floor | Integer | **Label**: Floor the call came from |
| destination_floor | Integer | **Feature**: Where user wants to go |
| day_of_week | Integer | **Feature**: Day of week (0-6) |
| hour_of_day | Integer | **Feature**: Hour of day (0-23) |

## API Endpoints

### POST /call
Call the elevator from a floor (triggers golden event logging if elevator is resting).

### POST /step
Advance simulation by one time unit.

### GET /status
Get current elevator status and total logs.

### GET /logs
Get demand logs for ML training.

### GET /stats
Get statistics for ML insights.

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python main.py
```
The server will start on `http://localhost:5000`

### Running Tests

```bash
python -m pytest test_elevator.py -v
```

### Running the Demo

```bash
python demo.py
```

The demo simulates a typical office building day and shows:
- Golden event capture
- ML data analysis

## ML Training Data

The system generates perfect training data for ML models:

### Features (X):
- `resting_floor`: Current resting floor
- `timestamp_rested`: When elevator became idle
- `day_of_week`: Day of the week (0-6)
- `hour_of_day`: Hour of the day (0-23)
- `destination_floor`: Where user wants to go (optional)

### Label (y):
- `call_floor`: The floor the next call comes from

### Example ML Use Cases:
- **Classification**: Predict most likely call floor
- **Regression**: Predict call probability for each floor
- **Time Series**: Predict call patterns over time

## Key Design Principles

1. **Focus on Golden Event**: Only log when elevator is resting and receives a call
2. **Discrete Time**: Step-based simulation for predictability and testing
3. **Single Table**: All ML data in one optimized table
4. **Time Features**: Automatic extraction of day_of_week and hour_of_day
5. **Simple API**: Minimal endpoints for simulation control

## Final notes
I have included the PDF "Elevator_Prediction_System_Design.pdf" explaining my proposed solution.