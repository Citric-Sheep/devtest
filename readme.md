![banner](readme_assets/banner.png)
# Smart Elevator Project
This is the solution for a challenge proposed by Citric Sheep, aiming to create an intelligent system for elevators. You can have a more detailed description of the challenge at the end of this readme.

## The solution
The intelligent system aims to choose the optimal floor for the elevator to rest, based on the elevator's call history. The system consists of a server that receives elevator calls and a database that stores these calls.

For this purpose, a heuristic algorithm has been proposed. Based on the call history, the algorithm selects the floor that has been called the most within a one-hour interval. Minimizing the following cost function:
```math
\text{cost(resting\_floor)} = \sum_{i=1}^{n} \text{calls}_{x_i} \times \lvert x_i - \text{resting\_floor} \rvert
```

Where $\text{calls}_{x_i}\$ is the number of calls for floor $x_i$ within the one-hour interval, and $n$ is the total number of floors.

The algorithm tests all possible floors and chooses the one that minimizes the cost function

For example, consider the following call history:
```
1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5
```

Organizing it into a call vector:
```
[3, 5, 6, 5, 1]
```

The algorithm tests all possible floors and chooses the one that minimizes the cost function. In this case, floor 3 (index 2) is the one that minimizes the cost function.

# How to run

## Setting up the environment
Create a virtual environment
```bash
python3.11 -m venv env
```

Activate the virtual environment
```bash
source env/bin/activate
```

Install the requirements
```bash
pip install -r requirements.txt
```

## Running the tests
```bash
pytest .
```

## Running the application
```bash
python main.py
```

## Running the server
```bash
python server.py
```

## The Challenge Description
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
