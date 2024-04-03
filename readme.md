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

# Proposed Solution for the Elevator Technical Test of Citric Sheep

## Additional Conditions:
- If an elevator is requested to go up or down, a floor should not be selected; otherwise, the system will indicate that it is an invalid move. This is done to simplify the logic.
- When the elevator is created, it is set as the default elevator and all movements are performed with it.
- Floors can range from negative integers allowed in Python to positive integers; however, 0 is not considered a floor. Example: The difference between floor -1 and floor 1 is only one floor.
- If another user requests the elevator during a trip only if is the same direction, it will stop there. However, if the user is going up and another user requests it in the opposite direction, it must wait until the trip upwards is finished; the same applies in reverse.
- The travel time per floor for this exercise will be one second.

## Models:
To solve this problem, two models are chosen. The first one is the elevator, which looks as follows:

```sql
TABLE elevator (
    Id INT PRIMARY KEY, -- Unique identifier of the elevator
    lower_floor INT, -- The lowest floor of the elevator
    top_floor INT, -- The highest floor of the elevator
    last_record_id INT, -- Reference to the last movement record
    is_up BOOLEAN, -- Indicates if the elevator is going up
    is_vacant BOOLEAN, -- Indicates if the elevator is available
    is_on_demand BOOLEAN -- Indicates if the elevator has been called
);
```
The next model refers to the records of each movement executed, and it looks as follows:

```sql
TABLE elevator_records (
    id INT PRIMARY KEY, -- Unique identifier of the record
    elevator_id INT, -- Reference to the elevator to which the record belongs
    current_floor INT, -- Floor at the time of boarding the elevator
    target_floor INT, -- Selected destination floor
    direction INT, -- Elevator direction
    movement_type VARCHAR, -- Indicates the type of movement, whether the elevator was called or a floor was selected
    demand_time TIMESTAMP, -- Time of elevator call
    arrival_time TIMESTAMP, -- Time of arrival at the destination floor
    is_vacant BOOLEAN -- Indicates if the elevator is available
);
```

### Clarification of Variables for "elevator_records":
It is important to clarify that since there are two types of movements, "CALL_ELEVATOR" and "MOVE_TO_FLOOR", some values may change their meaning depending on the type of movement.

If the movement type is "CALL_ELEVATOR", then the direction indicates the arrow the user pressed, i.e., up or down; "target_floor" will be the floor from which the user requested the elevator, "current_floor" is the floor where the elevator was located, "demand_time" refers to the time of the elevator call, and finally "arrival_time" refers to the time the elevator arrived at the requested floor. For the other type of movement "MOVE_TO_FLOOR" the values are maintained as shown in the model definition above.

## Application Testing
Three types of tests were developed:

1. The first one is the elevator behavior test "test_elevator_behavior.py", which is responsible for performing various movements, both incorrect according to the established rules, and stops and resting moments.
2. The second one, "test_crud_operations.py", is responsible for checking the basic CRUD functionalities. However, for the application's operation, some of these operations such as deletion are not necessary.
3. The third one is responsible for generating various movements with waiting times and completing them to have accuracy when generating useful information to predict the resting floor. Finally, the data that may be useful for training is stored in the "training_data" directory based on the data obtained from the app once the request is executed. This test is "test_elevator_training_records.py".

**IT IS OF VITAL IMPORTANCE THAT THE TESTS ARE RUN TOGETHER. THAT IS, THE FILE "TEST_ELEVATOR_BEHAVIOR.PY" IS RUN, AS THE TESTS HAVE DEPENDENCIES, AND LIKEWISE WITH EACH OF THE TWO REMAINING TEST FILES: "TEST_CRUD_OPERATIONS.PY", "TEST_ELEVATOR_TRAINING_RECORDS.PY".**


## Requirements to run de application
1. You must have python installed. In my case I use python version 3.12.
2. You must already have docker in your working environment.
3. You must clone the repository

You need to configure the root password for mysql in docker-compose.yml

```
version: '3.8'
services:
  mysqldb:
    image: mysql
    environment:
      - MYSQL_ROOT_PASSWORD={YOUR_PASSWORD}
    ports:
      - 3306:3306
```

In the same way you must have an .env file with the following environment variables:

```
DB_USER={YOUR_DB_USER}
DB_PASSWORD={YOUR_DB_PASSWORD}
DB_HOST={YOUR_MSQL_HOST}
DB_PORT={YOUR_PORT}
```
In this case, if you are running it locally, you can select the port as local once you are running mySql in your container.

The port for this configuration would be: 3306

## Running application
In the repository directory you must create a virtual environment:
`python -m venv venv`

Activates the virtual environment, in windows:
`venv\Scripts\activate`

Install python packages:
`pip install .\requirements.txt`

Run the docker command to be able to use the mysql database.
`docker compose up`

Once mySql is running, run the application in the "/elevator/app" directory

`python app.py`

You are ready to test the application.

## Running the test
You must be located in the directory "/elevator/test/" with the python virtual environment running:

You can run the tests one by one as follows:
```
pytest test_elevator_behavior.py
pytest test_crud_operations.py
pytest test_elevator_training_records.py
```