### Problem Understanding
The goal was to build a minimal backend system to record elevator demands and resting states, so that historical data can be used later by an ML model to predict the optimal resting floor.

### Design Decisions
1. Database Modeling
I created two tables:

Demand: stores the floor where the elevator was called and the timestamp.

ElevatorState: stores the elevator’s floor, timestamp, and whether it's vacant.

This separation allows:

Compare demand vs. elevator location.

Simulate a real scenario with frequent calls and elevator resting positions.

Alternative: I considered using a single table, but separating concerns made analysis easier and aligned with normalized schema practices.

2. API Endpoints
POST /api/demands: register a new demand.

POST /api/state: register the elevator’s current floor and availability.

GET /api/analytics: analyze the average distance between each recorded elevator state and the subsequent demand. This helps evaluate whether the elevator is frequently poorly positioned when idle.

This gives ML practitioners useful data such as:

Time series of elevator calls.

Reactions or delays from elevator states.

Or initiate a model retraining process to improve floor prediction accuracy based on updated behavior patterns.

3. Business Rules Added
In GET /analytics, we check if the elevator is often resting too far from the next demand, using a configurable threshold.

This acts as an early signal of poor optimization.

4. Testing
Covered endpoints with pytest and TestClient.

Verified status codes and response content.

Ensures system stability before plugging in any ML logic.

### Tech Stack
FastAPI + SQLite.

SQLAlchemy for ORM.

Pytest for testing.

