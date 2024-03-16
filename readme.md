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


**Problem and Project Objective:**

My project focuses on modeling an elevator system to optimize efficiency and user experience. When an elevator is empty and stationary between floors, I consider it in a "resting" state. My main goal is to determine the optimal resting floor to place the elevator based on the next probable floor from which the elevator will be called.

**Data Modeling:**

To address this problem, I have defined two fundamental data models:

1. **Demand:** This model represents service requests from elevator users. Each demand record contains information about the floor from which the request was made and the timestamp when the demand was created.

2. **Elevator Movement:** This model records elevator movements, including floor changes, actions taken (such as going up, going down, or being stopped), and estimated arrival times. It also stores the current state of the elevator, the floor requested by the user, and the next floor to which it is heading.

**Prediction and Data Engine:**

My project involves building a prediction engine that uses historical demand and elevator movement data to determine the optimal resting floor at any given time. This prediction engine analyzes patterns in historical data to identify trends and accurately predict the next floor from which the elevator will be called.

**Data Collection and Storage:**

To collect data, I have implemented endpoints within my application that record both user demands and elevator movements. This data is stored in a relational database, allowing me to efficiently manage large volumes of information and perform complex queries for analysis and prediction.

**Testing and System Verification:**

Verification and validation are critical components of my development process. I use comprehensive testing at all stages of the development lifecycle to ensure the stability, functionality, and performance of the system. I apply both automated and manual tests to verify each component of the system and ensure it meets the requirements and expectations of the end user.

Additionally, for the data engine, I have implemented a preprocessing function that analyzes historical elevator movement and user demand data. This function prepares the data for analysis and prediction by calculating the number of stops per floor and demand per floor, filtering floors with a minimum number of stops, and creating objects representing relevant information about the floors for subsequent use in predicting the optimal resting floor.

## Installation with Docker Compose
### Prerequisites
- Docker installed on your system.

### Steps to Follow
1. Clone this repository on your local machine:
   ```bash 
    git clone https://github.com/devtest/brahyanbedoya.git
   ```
2. Navigate to the project directory:
3. Create a `.env` file in the project's root directory:
    ```plaintext
    DATABASE_URL=postgresql://postgres:password@postgres:5432/elevator
    DB_USER=postgres
    DB_PASSWORD=password
    DB_NAME=elevator
    PGADMIN_DEFAULT_EMAIL=example@example.com
    ```
4. Run the following command to build and start the Docker containers:
    ```
    docker compose up --build
    ```
## Local Installation
1. Clone this repository on your local machine:
   ```bash 
    git clone https://github.com/devtest/brahyanbedoya.git
   ```
2. Run pip install -r requirements.txt.
3. Create a `.env` file in the project's root directory:
    ```plaintext
    DATABASE_URL=postgresql://postgres:password@postgres:5432/elevator
    DB_USER=postgres
    DB_PASSWORD=password
    DB_NAME=elevator
    PGADMIN_DEFAULT_EMAIL=example@example.com
    ```
4. Run the following command to execute the app
    ```
    py ./main.py
    ```
5. Access to the aplication
    ```
    http://localhost:5000
    ```
