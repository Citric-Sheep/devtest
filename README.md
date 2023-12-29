# Elevator Prediction Project

This project is a simple implementation of an elevator system with the goal of collecting data for a future machine learning prediction engine.

## Project Structure

```bash
.
├── README.md
├── main.py
├── original_readme.md
├── requirements.txt
├── src
│ ├── crud.py
│ └── models.py
└── tests
└── test_service.py
```


- **README.md**: The main documentation file for the project.
- **main.py**: The main FastAPI application file.
- **original_readme.md**: Original README file (contains the problem explanation).
- **requirements.txt**: File containing project dependencies.
- **src**: Directory containing source code.
  - **crud.py**: Module handling Create, Read, Update, Delete operations.
  - **models.py**: Module defining data models.
- **tests**: Directory containing test files.
  - **test_service.py**: Test file for the FastAPI service.

## Getting Started

1. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the FastAPI Application
    ```bash
    uvicorn main:app --reload
    ```
The FastAPI application will be running at http://127.0.0.1:8000.

## API Endpoints

The following endpoints are available in the Elevator Prediction API:

### 1. Call Elevator

- **Endpoint:** `/call-elevator`
- **Method:** `POST`
- **Description:** Simulates a call for the elevator.
- **Parameters:**
  - `target_floor` (int): The requested floor to go to.
  - `user_floor` (int): The floor where the user made the call.
- **Response:**
  - Success (200): Elevator called successfully.
  - Error (500): Error calling elevator.

### 2. Reset Elevator

- **Endpoint:** `/reset-elevator`
- **Method:** `DELETE`
- **Description:** Resets the elevator system by deleting all recorded elevator calls from the database.
- **Response:**
  - Success (200): Elevator reset successfully.
  - No calls exist (200): Elevator has not been called yet.

### 3. Get Elevator Calls

- **Endpoint:** `/get-elevator-calls`
- **Method:** `GET`
- **Description:** Retrieves a list of all elevator calls from the database.
- **Response:**
  - Success (200): Calls retrieved successfully along with the data.
  - No calls exist (200): Elevator has not been called yet.

### 4. Get Data as CSV

- **Endpoint:** `/get-data-csv`
- **Method:** `GET`
- **Description:** Retrieves elevator call data from the database and exports it to a CSV file.
- **Response:**
  - Success (200): Data exported to CSV file.
  - No calls exist (200): Elevator has not been called yet.

### API Documentation

Access the full API documentation, including request and response details, at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

