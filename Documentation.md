# CitricSheep Elevator System Documentation

## 1. Introduction
A brief overview of the elevator system project, its objectives, and key functionalities.

## 2. Requirements

- List of libraries and dependencies which can be installed from `requirements.txt`.

## 3. Installation and Setup

Follow these instructions to get the elevator control system up and running on your local machine for development and testing purposes.

### Clone the repository

First, clone the repository to your local machine:

bash
git clone https://github.com/rojored7/devtest.git
cd CitricSheep

#### Set up a Python virtual environment
It's good practice to use a virtual environment to isolate project dependencies. Here's how to set one up:
- For Windows:

python -m venv venv
.\venv\Scripts\activate

- For macOS and Linux:

python3 -m venv venv
source venv/bin/activate

#### Install dependencies
Install the project dependencies by running:

pip install -r requirements.txt

#### Initialize the database
Initialize the SQLite database using the provided schema:

sqlite3 database/elevator.db < database/schema.sql

This command will create a new SQLite database according to the schema.sql file.

## 4. Using the Application

- Running Tests
    To run the test suite and ensure everything is working as expected, execute:

    python main.py

    This script will run all the unit tests defined in the test directory and output the test results to the console.

- Starting the FastAPI app with Uvicorn: `uvicorn Api:app --reload`.
    The --reload flag enables auto-reloading of the server for development purposes.
    Once the server is running, you can view the auto-generated documentation and test the API endpoints by navigating to http://127.0.0.1:8000/docs in your web browser.


## 5. Project Structure
Explanation of the directory structure:
- `CRUD/`: Contains the `CRUD.py` module for CRUD operations.
- `database/`: Stores the database schema and SQLite file.
- `devtest/`: Development and testing related information.
- `src/service/`: Holds the elevator service logic (`elevator_service.py`).
- `test/`: Unit testing scripts.
- `venv/`: Python virtual environment (to be created locally).
- `Api.py`: The FastAPI application.
- `main.py`: Main script including application tests.
- `readme.md`: Detailed project documentation.

## 6. Data Model
Detailed description of the database schema (`schema.sql`). The relationship between tables and how the data relate to the elevator logic.


## 7. API Documentation
The FastAPI framework automatically generates interactive API documentation, including live testing of the API endpoints. There are two options for accessing this documentation:

http://127.0.0.1:8000/docs

In this interface, you will see an interactive UI where you can read about each API endpoint, the expected request bodies, query parameters, and the structure of response payloads. Additionally, you can directly interact with the API by sending requests from within the UI and view the responses.

### ReDoc

For an alternative documentation format, you can use ReDoc by going to:

http://127.0.0.1:8000/redoc

ReDoc provides a more traditional, static documentation layout, which some users may prefer for its readability and navigation features.

### Available Methods

Here is an overview of the available HTTP methods and their respective functionalities:

- `GET /trips/`: Retrieves a list of all recorded elevator trips from the database.
- `POST /trips/`: Creates a new elevator trip record. The request body must include the starting floor, ending floor, start time, end time, and a flag indicating whether it was a demand call.
- `PUT /trips/{trip_id}/`: Updates an existing elevator trip identified by `trip_id`. You can pass the new ending floor in the request body.
- `DELETE /trips/{trip_id}/`: Deletes an elevator trip record identified by `trip_id` from the database.

When you access the interactive documentation through `/docs`, you can execute these requests using the "Try it out" feature and view the live response from the API, which is helpful for understanding the behavior of your API endpoints.




