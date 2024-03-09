import datetime
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.main import app 
from app.routes import get_db
from app.models import ElevatorMovement, Demand
from app.schemas import ElevatorMovementCreate, DemandCreate

client = TestClient(app)

'''
+++++++++++++++++++++++++++++                    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   POST MOVEMENT    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                    +++++++++++++++++++++++++++++
''' 
def test_create_elevator_movement():
    # Define the data for testing
    elevator_movement_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "elevator_id": 1,
        "current_floor": 1,
        "next_floor": 2,
        "action": "move",
        "floor_requested": None,
        "expected_arrival_time": None  # Provide if available
    }
    
    # Make a POST request to create an elevator movement
    response = client.post("/elevator_movement/", json=elevator_movement_data)
    
    # Assert that the request was successful (HTTP status code 200)
    assert response.status_code == 200
    
    # Assert that the response data matches the expected data
    assert response.json()["current_floor"] == elevator_movement_data["current_floor"]
    assert response.json()["next_floor"] == elevator_movement_data["next_floor"]
    # Add more assertions as needed
    '''
+++++++++++++++++++++++++++++                    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   GET MOV BY ID    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                    +++++++++++++++++++++++++++++
''' 

def test_read_elevator_movement():
    # Make a GET request to read an elevator movement by ID
    response = client.get("/elevator_movement/1")
    
    # Assert that the request was successful (HTTP status code 200)
    assert response.status_code == 200
    # Add more assertions as needed

    '''
+++++++++++++++++++++++++++++                    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   GET MOV ALL    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                    +++++++++++++++++++++++++++++
''' 

def test_read_elevator_movements():
    # Make a GET request to read all elevator movements
    response = client.get("/elevator_movements/")
    
    # Assert that the request was successful (HTTP status code 200)
    assert response.status_code == 200
    # Add more assertions as needed

    '''
+++++++++++++++++++++++++++++                    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   PUT MOV BY ID    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                    +++++++++++++++++++++++++++++
''' 

def test_update_elevator_movement():
    # Define the data for updating an elevator movement
    updated_data = {
        "current_floor": 3,
        "next_floor": 4
    }
    
    # Make a PUT request to update an elevator movement by ID
    response = client.put("/elevator_movement/1", json=updated_data)
    
    # Assert that the request was successful (HTTP status code 200)
    assert response.status_code == 200
    # Add more assertions as needed


'''
+++++++++++++++++++++++++++++              +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   DEMANDS    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++              +++++++++++++++++++++++++++++
''' 
def test_create_demand():
    # Define the data for testing
    demand_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "floor_requested": 5
    }
    
    # Make a POST request to create a demand
    response = client.post("/demand/", json=demand_data)
    
    # Assert that the request was successful (HTTP status code 200)
    assert response.status_code == 200
    
    # Assert that the response data matches the expected data
    assert response.json()["floor_requested"] == demand_data["floor_requested"]
    # Add more assertions as needed

# Add more test functions as needed
