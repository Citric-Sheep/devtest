# Dev Test Solution

## Elevators

The idea is to store the elevator calls, a timestamp and the floor it will go in the next movement. With this, we can evaluate how many movements the elevator did, which floors are the most used and which time of day are the most busy. 
I created an API using FastAPI to handle two endpoints, one to simulate the elevator movement from one floor to the other, the other endpoint is to generate a csv file with this information. I designed this to be as simple as possible. 
Business rules: 
- The elevator can only go to floors 1-10. 
- The elevator will respond with a 422 code if the call is repeated (Someone from the 2nd floor wants to go to the 2nd floor, for example)