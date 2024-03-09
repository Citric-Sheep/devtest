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







## Description
The Elevator Predictor is a web application developed with Python and FastAPI that provides functionalities for predicting elevator traffic in a building. It uses elevator movement data and user demand data to make these predictions and optimize elevator performance.

## Features
- Creation of Elevator Movements: Allows registering elevator movements, including actions like moving and calling the elevator from a floor.
- Visualization of Elevator Movements: Provides endpoints to query and visualize registered elevator movements.
- Creation and Management of User Demands: Allows registering user demands to use elevators from different floors.
- Data Preprocessing: Offers an endpoint to preprocess elevator movement and user demand data, calculating the number of stops per floor and the number of demands per floor.
- Elevator Traffic Prediction: Uses machine learning algorithms to predict elevator traffic based on processed data.

## Technologies Used
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pandas
- Scikit-learn

## Installation and Usage
1. Clone this repository on your local machine.
2. Install project dependencies by running `pip install -r requirements.txt`.
3. Configure environment variables in a `.env` file with your database credentials.
4. Run the application with `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`.
5. Access the application through your web browser at `http://localhost:8000`.

## Main Endpoints
- `/elevator_movement/`: Allows creating and managing elevator movements.
- `/demand/`: Allows creating and managing user demands.
- `/predictor/preprocessing`: Performs data preprocessing for elevator traffic prediction.

## Accessing PGAdmin and Load Balancing with Nginx
- **PGAdmin Access:** You can connect to PGAdmin through port 5000. Simply access your web browser and enter `http://localhost:5000`.
- **Load Balancing with Nginx:** This project includes a reverse proxy with Nginx to balance the load. Nginx is configured to listen on port 80. To access the application through Nginx, use `http://localhost`.
## Contribution
Contributions are welcome! If you want to contribute to this project, please follow the steps described in the `CONTRIBUTING.md` file.

## Authors
- Camilo Castrillon-Calderon

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Installation with Docker Compose
### Prerequisites
- Docker installed on your system. You can download it from [here](https://www.docker.com/get-started).

### Steps to Follow
1. **Clone this repository on your local machine:**
   ```bash
   git clone https://github.com/ccastri/devtest.git
2. Navigate to the project directory:
3. Create a `.env` file in the project's root directory with the following environment variables:
    ```plaintext
    DB_HOST=database
    DB_PORT=5432
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name
    PGADMIN_DEFAULT_EMAIL=your_email@example.com
    ```

4. Run the following command to build and start the Docker containers:
    ```
    docker compose up --build
    ```
