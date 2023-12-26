<a name="readme-top"></a>
[![Python template](https://github.com/DavidNavarroSaiz/Elevator_data_generator/actions/workflows/main.yml/badge.svg)](https://github.com/DavidNavarroSaiz/Elevator_data_generator/actions/workflows/main.yml)



<!-- PROJECT LOGO -->

<h3 align="center">Elevator Data Generator</h3>

  <p >
This project is a solution for the elevator data generator problem proposed in the following github repository: https://github.com/Citric-Sheep/devtest
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


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


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* python
* docker
* PostgreSQL
* FastAPI

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

Make sure you have the following prerequisites installed:

- Python (3.7 or higher)
- Git (for version control)
- PostgreSQL
- Docker

* It is recommended to create your own environment for this project:


### Installation
1. Clone the repository to your local machine:

    ```
    git clone https://github.com/DavidNavarroSaiz/Elevator_data_generator
    ```

2. Navigate to the project directory:

    ``` 
    cd your-project
    ```

3. Install project dependencies using `pip`:

    ```
    pip install -r requirements.txt
    ```

4. setup the environment variables:
    Follow these steps to set up the necessary environment variables for your project:
    create a new database in PostgreSQL 

    Create a new file named .env in the root directory of your project.

    Open the .env file and add the following line with the URL with the connection with the database:


    ```
    DATABASE_URL="postgresql://postgres:david.123@localhost:5432/<DATABASE_NAME>"
    ```
    replace the <DATABASE_NAME> with your own database name
    Save the .env file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### Generator Setup
Data generation deppends on the variables found in the 'elevator_variables.json' file, where you can find the following variables:
* floor_capacities (dict): Mapping of floor types to capacities. Right now there are configured the following 4 floor types, but you can add other floor_types if needed:
   
    "Residential": a floor designed for people houses, where usually people live
    "Social": community spaces where all the people of the building can access
    "entrance": it is the entrance of the building, usually it is the first floor of the building 
    "Company": it is a floor for working companies or bussiness offices 

    the dictionary seems like this:
    ```
    "floor_capacities": {
    "Residential": 20,
    "Social": 100,
    "entrance": 200,
    "Company": 40
  }
  ```
  in front of each key of the dictionary there is the capacity for that specific floor, so configure it based on the number of rooms per floor, bussiness employes, social spaces capacity and number of users of the elevator.
  in this case the dictionary is telling us that the 
  residential floors, usually have 20 people, which is in average 5 houses pero room.
  social_floors, have a capacity of 100 people, which is a common value for pools, game rooms, or flat roof.
  entrance: it is the capacity of people entering daily.
  company: it means that there is a company with 40 employees.


* floor_types (dict): Mapping of floor numbers to floor types. this dictionary selects what are the floors that have special types, so for example in the following case:
```
  "floor_types": {
    "1": "entrance",
    "10": "Social",
    "2": "Company"
  },
```
it means that the first floor is the entrance of the building , that the 10th floor is a social space, and in the 2nd floor there is a company .
all the floors that arent mentioned are per default a residential floor.

* rows_generated (int): Number of elevator states to generate. it is the lenght of the generated data.
* floor_number (int): Total number of floors in the building. 

* min_time_interval_seconds (int): Minimum time interval in seconds between elevator states. by defaul the time that it takes from a floor next to other is 10 seconds
* max_time_interval_seconds (int): Maximum time interval in seconds between elevator states. it is the time between the first floor and the last floor, for modelling the default value is 30 seconds
* interval_per_floor_seconds (float): Time interval per floor in seconds. this is the time that it takes the elevator to move from a floor to other next to it once it reached the travel velocity.
* peak_hours (list): List of dictionaries representing peak hours intervals. in this case:
  ```
    "peak_hours":[{"start": 6, "end": 8},
          {"start": 12, "end": 14},
          {"start": 17, "end": 20}],
  ```
  it means that from 6 to 8, from 12- 14 and 17-20 it is peak hours, what it does in the generation model is that the delta datetime between each state of the elvator is multiplied by the 'peak_multiplier'

* peak_multiplier (float): Multiplier for peak hours intervals. by default it is 0.5, meaning that in peak hours there is the double of activiity in the elvator than others.
* random_minutes_range (dict): Range of random minutes added to intervals. generated data has a delta of time between each row or state of the elevator, that delta of time is a random number that is between the range set in this variable:
  ```
  "random_minutes_range": {"min": 0, "max": 5}
  ```

in this case it is generating data between 0 minutes and 5 minutes, so it means that in the data generation you will only find changes of time as maximum as 5 minutes, meaning that a people uses the elevator 5 minutes after other person used it.
of course if it is peak_time, that range is multiplied by the peak_multiplier, making it an smaller range of time.



### Using the FastAPI Service

To use the FastAPI service for interacting with the chatbot, follow these steps:

1. Run the FastAPI service:

    ```
    python main.py
    ```
    or using the console:

    ```
    uvicorn main:app --reload --port 8000
    ```

2. The service will start on a specified port (typically 8000). You can access the API endpoints using tools like `curl` or API testing platforms.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Using the docker:

a docker-compose.yml is used to create the database called "my_dev_database" but it can be changed you can also run the following command:
```
 docker-compose up --build
```

it will create a docker image with the database and the fastapi app.


In both cases you can acces to the fastAPI documentation and usage in the  specified port(typically 8000)
```
http://127.0.0.1:8000/docs#

```

# FastAPI Endpoints Documentation

This documentation provides details about the endpoints available in the FastAPI project.

## Run Generator Endpoint

### Endpoint: `/run-generator`

**Description:**  
Executes the elevator state generator.

## Delete All Rows Endpoint

### Endpoint: /delete-all-rows
**Description:**  
Deletes all elevator state rows from the database.

HTTP Method: GET

## Get All Rows Endpoint
### Endpoint: /get-all-rows
**Description:**  
Retrieves all elevator state rows from the database.

## Save to CSV Endpoint

### Endpoint: /save-to-csv
**Description:**  
Saves all elevator state rows to a CSV file and allows users to download it.