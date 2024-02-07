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


## Solution Summary
All of the codes were implemented in Ubuntu (WSL, specifically), without needing to install any new libs, aside from the ones that already comes with a new python evnironment.

1 - Modeling the Problem into a Storage Schema (SQL DB Schema or Whatever You Prefer):

For this problem, I modeled the data using two main entities (Classes): Elevator and Demand. The Elevator entity includes attributes like `elevator_id`, `current_floor`, `resting_floor`, and `elevator_status`. The Demand entity includes attributes like `demand_id`, `floor`, and `timestamp`. Both entities have methods to convert objects to dictionaries for easy storage and retrieval.

The storage schema is implemented using SQLite as a simple database solution. I created tables for elevators and demands, allowing for the storage and retrieval of data efficiently. The choice of SQLite makes it easy to demonstrate the CRUD operations and can be a starting point for more complex databases if needed.

2 - CRUD Some Data:

I provided implementations for CRUD operations in both the ElevatorService and DemandService (Classes). These services interact with the SQLite database to create, retrieve, and delete elevators and demands, plus the option to specifically update the elevator, as it would seem similar to a real case scenario. Sample data is created and manipulated in the "main_db_test_br.py" script to showcase these CRUD operations.

3 - Add Some Flair with a Business Rule or Two:

I added the business rule that when there are demands on the current floor of the elevator, it "doesn't move" (it doesn't changeits current floor). This is reflected in the ElevatorService where the 'update_elevator' method allows for changing the `current_floor`, `resting_floor`, and `elevator_status` attributes. Also, here it is shown the concept of a resting floor, being crucial for determining the ideal position for an elevator to wait when Idle and should be better developed later in this projetc with the use of machine learning prediction algorithms, once having a satisfactory database for the algorithm to learn.

4 - Have the Data in a Suitable Format to Feed to a Prediction Training Algorithm:

I ensured that the data is structured and stored in a suitable format for feeding into a prediction training algorithm. The data is stored in tables with clear structures, making it easy to extract and transform into the necessary format for training machine learning models. The 'to_dict' and 'from_dict' methods in the models facilitate easy conversion to and from dictionaries.

5 - Provide Storage of Some Sort (SQLite):

I used SQLite as the storage solution, creating an in-memory database for testing purposes. The ElevatorService and DemandService interact with this SQLite database, demonstrating the storage and retrieval of data. The use of SQLite provides a lightweight and straightforward storage solution, but it could be replaced with more robust databases of choice if necessary, this one was just used for test.

6 - Tests Covering the Code and Useful in a Prod System:

I provided test scripts ("test_elevator_service.py", "test_demand_service.py") using the unittest module to cover various functionalities in the ElevatorService and DemandService. Also I did one last script (the "main_db_test_br.py") which maintain a database (named database.sqlite) via sqlite (being necessary to install sqlite3 via `sudo apt install sqlite3`, if your in Ubuntu). These tests check the creation, retrieval, updating, and deleting of elevators and demands. They are useful for verifying the correctness of the implemented features and can be extended for future development.

In summary, the solution addresses the requirements by modeling the problem, implementing CRUD operations, incorporating business rules, storing data in a suitable format, using SQLite for storage, and providing comprehensive tests. The simplicity of the solution aligns with the emphasis on creating a fit-for-purpose system within a reasonable timeframe.

## Code usage
Since this project was developed via WSL (Ubuntu), it was necessary to follow these steps:

### Install Conda:

If you haven't installed Conda yet, you can download and install [Miniconda](https://docs.anaconda.com/free/miniconda/) or [Anaconda](https://www.anaconda.com/) from the official website.

### Create a New Conda Environment:

Open a terminal window and run the following commands to create and run a new Conda environment named elevator_prediction:

```bash
# Create a new Conda environment with the most updated Python installed.
conda create -n elevator_prediction

# Activate the Conda Environment:
conda activate elevator_prediction

# Install necessary dependencies (not necessary in for the moment, since only using built-in lib from python)
pip install -r requirements.txt
```

Also, for some systems, it is necessary to install SQLite with the following command on terminal:
```bash
sudo apt install sqlite3
```

### Running the main codes
For simplicity, the main codes are on root of the Project, facilitating to run them via terminal.
Prints within scripts are merely used as a way of better clarification for proccesses steps and tests, being optional for an effective code usage.

#### Unit Tests
The project includes unit tests for both DemandService and ElevatorService. To run the unit tests, execute the following commands:

```bash
python test_demand_service.py
python test_elevator_service.py
```

#### Main Script (main_db_test_br.py)
The main script main.py demonstrates the features of the Elevator Prediction Project. It showcases the creation, retrieval, updating, and deletion of elevators and demands. To run the main script, execute the following command:
```bash
python main_db_test_br.py
```

Once executated the main python code, it can be noticed that a database with the name of "database.sqlite", within folder "data", is created (or updated if already present). There, it shall contain all the generated and managed data about the Elevators and the Demands. 

#### Dataset (data/database.sqlite)
An small example database was uploaded to this repository. It can be accessed via terminal using the following codes:

```bash
#Opens the SQLite command-line interface and connects to the SQLite database
sqlite3 database.sqlite
```

Once oppend the SQLite command-line, Elevator and Demand can be visualized via the following codes:

```bash
# Check the structure of the elevators table
.schema elevators

# Retrieve all rows from the elevators table
SELECT * FROM elevators;

# Check the structure of the demands table
.schema demands

# Retrieve all rows from the demands table
SELECT * FROM demands;
```
And many other commands if you know SQL language.
Once desired to leave the SQLite command-line, just use the following code on terminal:

```bash
.exit
```

Keep in mind that this code can be much further developed with enough time and data, and what is seen here is the result of 4 hours of work syntesized to show a more presentative approach.

Best regards to whom it may concern,
Guilherme Coelho Fermino.
