# Dev Test

## Elevators
When an elevator is empty and not moving this is known as it's resting floor.
The ideal resting floor to be positioned on depends on the likely next floor that the elevator will be called from.

We can build a prediction engine to predict the likely next floor based on historical demand, if we have the data.

The goal of this project is to model an elevator and save the data that could later be used to build a prediction engine for which floor is the best resting floor at any time
- When people call an elevator this is considered a demand
- When the elevator is vacant and not moving between floors, the current floor is considered its resting floor
- When the elevator is vacant, it can stay at the current position or move to a different floor
- The prediction model will determine what is the best floor to rest on


_The requirement isn't to complete this system but to start building a system that would feed into the training and prediction
of an ML system_

You will need to talk through your approach, how you modelled the data and why you thought that data was important, provide endpoints to collect the data and
a means to store the data. Testing is important and will be used verify your system


#### In short
This is a domain modeling problem to build a fit for purpose data storage with a focus on ai data ingestion
- Model the problem into a storage schema (SQL DB schema or whatever you prefer)
- CRUD some data
- Add some flair with a business rule or two
- Have the data in a suitable format to feed to a prediction training algorithm

---

#### To start
- Fork this repo and begin from there
- For your submission, PR into the main repo. We will review it, a offer any feedback and give you a pass / fail if it passes PR
- Don't spend more than 4 hours on this. Projects that pass PR are paid at the standard hourly rate

#### Marking
- You will be marked on how well your tests cover the code and how useful they would be in a prod system
- You will need to provide storage of some sort. This could be as simple as a sqlite or as complicated as a docker container with a migrations file
- Solutions will be marked against the position you are applying for, a Snr Dev will be expected to have a nearly complete solution and to have thought out the domain and built a schema to fit any issues that could arise
A Jr. dev will be expected to provide a basic design and understand how ML systems like to ingest data


#### Trip-ups from the past
Below is a list of some things from previous submissions that haven't worked out
- Built a prediction engine
- Built a full website with bells and whistles
- Spent more than the time allowed (you won't get bonus points for creating an intricate solution, we want a fit for purpose solution)
- Overcomplicated the system mentally and failed to start

# Elevator API


#### How to set up the elevator API

```
"clone the repository"
git clone <repository url>
"Create virtual environment for the project(optional but recomended)"
python -m venv <env_name>
"Activate the virtual environment"
<env_name>\Scripts\activate
"Install project dependencies"
pip install -r requirements.txt
"Move to project folder"
cd .\elevator_api\
"Start the API"
python manage.py runserver
"Run tests"
python manage.py test elevator.tests
```


#### How to use the elevator API
 - The elevator API consists on different endpoints to CRUD the models planned to participate on the elevator system and to generate the data that would feed into the machine learning model
 - The main data for the Ml model is the data represented by the movement model, you can acces it on the elevator_movement table
 - To generate data you must first create a elevator and a person, then you need to create a ElevatorCall object instance and then call the move_elevator view passing the created person, elevator and ElevatorCall data
 - The base endpoint for the api calls are `http://127.0.0.1:8000/elevator_api/`, to call the views use the following syntax: `http://127.0.0.1:8000/elevator_api/<model_prefix>/<view_name>/`


# Person ViewSet

## Overview

The `PersonViewSet` is a Django Rest Framework ViewSet designed for CRUD operations on instances of the `Person` model. It provides endpoints for creating, deleting, updating, and retrieving individual persons, as well as getting a list of all persons. The endpoint prefix to access the `PersonViewSet` is `/person/`.

## Endpoints

### Create Person

- **Endpoint**: `/person/create_person/`
- **Method**: POST
- **Description**: Create a new person instance.
- **Request Body**: JSON data representing a new person.
- **Success Response**:
  - Status Code: 201 Created
  - Body: Serialized data of the created person.

### Delete Person

- **Endpoint**: `/person/delete_person/`
- **Method**: DELETE
- **Description**: Delete a person by providing the person's ID.
- **Request Body**: JSON data with the ID of the person to be deleted.
- **Success Response**:
  - Status Code: 204 No Content
  - Body: `{ "message": "Person deleted successfully" }`
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Person not found" }`

### Get Person

- **Endpoint**: `/person/get_person/`
- **Method**: GET
- **Description**: Retrieve details of a specific person using their ID.
- **Parameters**: Query parameter `id` specifying the person's ID.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of the requested person.
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Person not found" }`

### Update Person

- **Endpoint**: `/person/update_person/`
- **Method**: POST
- **Description**: Update details of a person by providing the person's ID and updated data.
- **Request Body**: JSON data with the ID of the person to be updated and the updated fields.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of the updated person.
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Person not found" }`

### Get People

- **Endpoint**: `/person/get_people/`
- **Method**: GET
- **Description**: Retrieve a list of all persons.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of all persons.

## Error Handling

In case of errors, the response body will contain an `error` field providing information about the issue.

# Movement ViewSet

## Overview

The `MovementViewSet` is a Django Rest Framework ViewSet designed for CRUD operations on instances of the `Movement` model. It provides endpoints for creating, deleting, updating, and retrieving individual movements, as well as getting a list of all movements. The endpoint prefix to access the `MovementViewSet` is `/movement/`

## Endpoints

### Get Movement

- **Endpoint**: `/movement/get_movement/`
- **Method**: GET
- **Description**: Retrieve details of a specific movement using its ID.
- **Parameters**: Query parameter `id` specifying the movement's ID.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of the requested movement.
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Movement not found" }`

### Delete Movement

- **Endpoint**: `/movement/delete_movement/`
- **Method**: DELETE
- **Description**: Delete a movement by providing the movement's ID.
- **Parameters**: Query parameter `id` specifying the movement's ID.
- **Success Response**:
  - Status Code: 204 No Content
  - Body: `{ "message": "Movement deleted successfully" }`
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Movement not found" }`

### Create Movement

- **Endpoint**: `/movement/create_movement/`
- **Method**: POST
- **Description**: Create a new movement instance.
- **Request Body**: JSON data representing a new movement.
- **Success Response**:
  - Status Code: 201 Created
  - Body: `{ "message": "Movement created successfully" }`
- **Error Response**: Same as the default create endpoint.

### Update Movement

- **Endpoint**: `/movement/update_movement/`
- **Method**: POST
- **Description**: Update details of a movement by providing the movement's ID and updated data.
- **Request Body**: JSON data with the ID of the movement to be updated and the updated fields.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of the updated movement.
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Movement not found" }`

### Get Movements

- **Endpoint**: `/movement/get_movements/`
- **Method**: GET
- **Description**: Retrieve a list of all movements.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of all movements.

## Error Handling

In case of errors, the response body will contain an `error` field providing information about the issue.

# ElevatorCall ViewSet

## Overview

The `ElevatorCallViewSet` is a Django Rest Framework ViewSet designed for CRUD operations on instances of the `ElevatorCall` model. It provides endpoints for creating, deleting, updating, and retrieving individual elevator calls, as well as getting a list of all elevator calls. The endpoint prefix to access the `ElevatorCallViewSet` is `/elevator_calls/`

## Endpoints

### Get Call

- **Endpoint**: `/elevator_calls/get_call/`
- **Method**: GET
- **Description**: Retrieve details of a specific elevator call using its ID.
- **Parameters**: Query parameter `id` specifying the elevator call's ID.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of the requested elevator call.
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Call not found" }`

### Delete Call

- **Endpoint**: `/elevator_calls/delete_call/`
- **Method**: DELETE
- **Description**: Delete an elevator call by providing the call's ID.
- **Parameters**: Query parameter `id` specifying the call's ID.
- **Success Response**:
  - Status Code: 204 No Content
  - Body: `{ "message": "Call deleted successfully" }`
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Call not found" }`

### Create Call

- **Endpoint**: `/elevator_calls/create_call/`
- **Method**: POST
- **Description**: Create a new elevator call instance.
- **Request Body**: JSON data representing a new elevator call.
- **Success Response**:
  - Status Code: 201 Created
  - Body: Serialized data of the created elevator call.
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "Status": "call not found" }` (if the specified elevator ID is not found)
  - Status Code: 400 Bad Request
  - Body: `{ "Status": "Origin or target floor is out of bounds" }` (if origin or target floor is out of bounds)

### Update Call

- **Endpoint**: `/elevator_calls/update_call/`
- **Method**: POST
- **Description**: Update details of an elevator call by providing the call's ID and updated data.
- **Request Body**: JSON data with the ID of the call to be updated and the updated fields.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of the updated elevator call.
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "ElevatorCall not found" }`

### Get Calls

- **Endpoint**: `/elevator_calls/get_calls/`
- **Method**: GET
- **Description**: Retrieve a list of all elevator calls.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of all elevator calls.

## Error Handling

In case of errors, the response body will contain an `error` field providing information about the issue.

# Elevator ViewSet

## Overview

The `ElevatorViewSet` is a Django Rest Framework ViewSet designed for CRUD operations on instances of the `Elevator` model. It provides endpoints for creating, deleting, updating, and retrieving individual elevators, as well as getting a list of all elevators. Additionally, it generates the data for the ML model. The endpoint prefix to access the `ElevatorViewSet` is `/elevator/`

## Endpoints

### Get Elevator

- **Endpoint**: `/elevator/get_elevator/`
- **Method**: GET
- **Description**: Retrieve details of a specific elevator using its ID.
- **Parameters**: Query parameter `id` specifying the elevator's ID.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of the requested elevator.
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Elevator not found" }`

### Delete Elevator

- **Endpoint**: `/elevator/delete_elevator/`
- **Method**: DELETE
- **Description**: Delete an elevator by providing the elevator's ID.
- **Parameters**: Query parameter `id` specifying the elevator's ID.
- **Success Response**:
  - Status Code: 204 No Content
  - Body: `{ "message": "Elevator deleted successfully" }`
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Elevator not found" }`

### Create Elevator

- **Endpoint**: `/elevator/create_elevator/`
- **Method**: POST
- **Description**: Create a new elevator instance.
- **Request Body**: JSON data representing a new elevator.
- **Success Response**:
  - Status Code: 201 Created
  - Body: Serialized data of the created elevator.
- **Error Response**:
  - Status Code: Varies
  - Body: Serialized errors if the input data is invalid.

### Update Elevator

- **Endpoint**: `/elevator/update_elevator/`
- **Method**: POST
- **Description**: Update details of an elevator by providing the elevator's ID and updated data.
- **Request Body**: JSON data with the ID of the elevator to be updated and the updated fields.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of the updated elevator.
- **Error Response**:
  - Status Code: 404 Not Found
  - Body: `{ "error": "Elevator not found" }`

### Get Elevators

- **Endpoint**: `/elevator/get_elevators/`
- **Method**: GET
- **Description**: Retrieve a list of all elevators.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Serialized data of all elevators.

### Call Elevator

- **Endpoint**: `/elevator/call_elevator/`
- **Method**: POST
- **Description**: Initiate an elevator movement based on an elevator call, updating the elevator's position and generating a movement record.
- **Request Body**: JSON data representing the elevator call, elevator, and person involved.
- **Success Response**:
  - Status Code: 200 OK
  - Body: Information about the completed elevator movement, including the movement record.
- **Error Response**:
  - Status Code: Varies
  - Body: Serialized errors or additional status information.

## Error Handling

In case of errors, the response body will contain an `error` field providing information about the issue.
