
# MY THOUGHT PROCESS
### Whenever im faced with an AI modeling problem, i often love to revert to the fundamentals of developing models then expand from there, i have found this to be a good way to approach problems in a methodical and structured way, because anything that can be broken down into a process can be meausred and anything that can be measured can be improved, this i believe is the very heart of artifiicial intelligence

### My methodical steps are as follows:

### 1. Identify and fully understand the problem 

### 2. Identify the prediction target or goal

### 3. Identify the available data that we have access to

### 4. Identify obvious and non-obvious factors that could influence the prediction target

### 5. Select the appropriate model that would help best solve the problem, understand its limitations and constraints as well as strategies and techniques to improve performance

### 6. Prepare the data for training and testing 

### 7. Evaluate the models performance and based on results decide whether to iterate and improve training data or use a different approach and model entirely and keep iterating and benchmarking, understanding trade offs and beneffits between approaches



# Elevator resting floor prediction model solution

## Problem statement:
### From my understanding were trying to predict the best possible floor the elevator should rest on according to certain factors such as time of day, week, month, season, etc in order to anticipate which floor demand will possibly come from next so we can provide the best possible and efficient service for users in that particular building

## Prediction target:
### In order to not only predict the next possible floor at a particular time but provide probabilitiies for all floors at a particular time, i would go for a mutliclass outcome, i think this would allow the elevator to be adjusted to a certain level of accuracy as desired by users


## What factors  could possibly influence the demand of the elevator (both obvious and non obvious)
- ### Time of day:
  #### We might find that there is a higher demand on certain floors in the mornings, lunch or evenings, e,g a working building where people need the elevator closer to ground floors as people come into work and closer to certain floors as people leave  work or go out for lunch

- ### Day of the week
  #### We might find that more people come into work on monday mornings as compared to friday, if the building is multipurpose, certain floors might have  working people coming in while other days house residents and thus less activity on certain floors 
- ### Week of the month 
  #### We might discover that certain weeks of the month have more people/traffic as compared to other weeks, e.g retreats, field work weeks, etc
- ### Maintainance schedule that week (if any)
  #### This is one of those non obvious factors, we might discover that an elevator that is not regularly maintained is less trusted by users and so they decide maybe to take the stairs, only users that need to travel safer distances might prefer it, e.g  a floor above the ground floor, this would also help avoid overfitting and help our model generalize better
- ### Elevator load
  #### We might find that when the elevator is heavy, at a particular time, the elevator tends to move to a certain floor with more people in it.

- ### Current weather season
  #### We might find that during winter, christmas or summer, users might not prefer the elevator, or certain floors experience more demand

- ### Current elevator floor
  #### This is another one of those non obvious ones, naturally i wouldnt think a current elevator floor could influence where people would like to go next, but maybe we might discover a pattern of if the elevator is called from the ground floor at a particular time, users are moving to a working floor for example in a multipurpose  building

- ### Number of calls that day on all floors
  #### Understanding how many calls are made on each floor in a day could help us decipher busy floors, this could in our overall prediction, during live prediction this could be accumulated through the day live.

## Data access 
  ### Next i need to understand what historical data can actually be collected and fed into our system during training  as well as the kind of data that the system will have access to during actual live prediction, the availability of data affects or constraints the model we want to use.
  ### Data such as time of day, day of week, week of month, maintainance schedule and current weather season are available natively to our system and can be enhanced by installing addidtional packages, other remaining feattures are usually available in elevator systems
  ### With the kind of data i have access to, now would be the best time to plan the model that would work well with this data, i would research  on best performing models for my use case and available data as well as time-frame, and in my current scenario that would a Gradient boosting model, specifically CatBoost which has been known to work well with categorical features such as day of week, etc without needing encoding. In terms of timeframe, the categorical handling conveniennce of CatBoost often outweighs the speed cost, my second alternative  would be Random forest, with the drawback of having to manually encode categorical features. 


## Storage Schema

### For the storage schema i would create a relational database with the following entities and relationships, 

### - Building: Meta data about the building with a one to many relationship with the Elevator, because buildings ideally hold  elevators
### - Elevator: Meta data about the elevator with a one to many relationship too ElevatorCall

### - ElevatorCall: Meta data about the elevator call with a many to one relationship with the Elevator to track call demands









