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
- ### Current weather season
- #### We might find that during winter, christmas or summer, users might not prefer the elevator, or certain floors experience more demand


### Data access 
#### Next i need to understand what historical data can actually be collected and fed into our system during training  as well as the kind of data that the system will have access to during actual live prediction
#### Data such as time of day, day of week, week of month, maintainance schedule and current weather season are available natively to our system and can be enhanced  by installing addidtional packages.






