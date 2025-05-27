
# MY THOUGHT PROCESS
### Whenever im faced with an AI modeling problem, i often love to revert to the fundamentals of developing models then expand from there, i have found this to be a good way to approach problems in a methodical and structured way, because anything that can be broken down into a process can be measured and anything that can be measured can be improved, this i believe is the very heart of artifiicial intelligence

### My methodical steps are as follows:

### 1. Identify and fully understand the problem 

### 2. Identify the prediction target or goal

### 3. Identify the type of available data that we have access to

### 4. Identify obvious and non-obvious factors that could influence the prediction target

### 5. Select the appropriate model that would help best solve the problem, understand its limitations and constraints as well as research strategies and techniques to improve performance

### 6. Prepare the data for training and testing 

### 7. Evaluate the models performance and based on results and decide whether to iterate and improve training data or use a different approach and model entirely and keep iterating and benchmarking, understanding trade offs and benefits between approaches



# Elevator resting floor prediction model solution

## 1. Problem statement:
### From my understanding were trying to improve the efficiency and service delivery of a buildings elevator by predicting the best floor for the elevator to rest in-between calls. 


## 2. Prediction target:
### The building consists of multiple floors, and because of this multiple options to consider when predicting the best floor to rest in-between calls, i believe a multiclass predicition target would be the best option for this problem because it not only gives us alternatives but levels of accuracy we can use to adjust service delivery. 

## 3. Available data:
### The data we have available is as follows:

- ### Time of day
- ### Day of week
- ### Week of month
- ### Maintainance schedule (if any)
- ### Elevator load
- ### Current weather season
- ### Current elevator floor

## 4. What factors could possibly influence the demand of the elevator (both obvious and non obvious)
- ### Time of day:
  ### We might find that there is a higher demand on certain floors in the mornings, lunch or evenings, e.g a working building where people need the elevator closer to ground floors as people come into work and closer to certain floors as people leave  work or go out for lunch

- ### Day of the week
  ### We might find that more people come into work on monday mornings as compared to friday, if the building is multipurpose, certain floors might have  working people coming in while other days house residents and thus less activity on certain floors 
- ### Week of the month 
  ### We might discover that certain weeks of the month have more people/traffic as compared to other weeks, e.g retreats, field work weeks, etc
- ### Maintainance schedule (if any)
  ### This is one of those non obvious factors, we might discover that an elevator that is not regularly maintained is less trusted by users and so they decide maybe to take the stairs, only users that need to travel safer distances might prefer it, e.g  a floor above the ground floor, this would also help avoid overfitting and help our model generalize better
- ### Elevator load
  ### We might find that when the elevator is heavy, at a particular time, the elevator tends to move to a certain floor with more people in it.

- ### Current weather season
  ### We might find that during winter, christmas or summer, users might not prefer the elevator, or certain floors experience more demand

- ### Current elevator floor
  ### This is another one of those non obvious ones, naturally i wouldnt think a current elevator floor could influence where people would like to go next, but maybe we might discover a pattern of if the elevator is called from the ground floor at a particular time, users are moving to a working floor for example in a multipurpose  building



## Model Selection
### Since i now know our problem, prediction target, available data as well as influencing factors towards our prediction target, both obvious and non-obvious, i would research on the best model for the job, which i found to be the CatBoost model, reason being it handles categorical features such as days of week, etc without needing encoding, this to me is the best place to start experimenting and testing an ideal model for the problem at hand.


## Prepare data for training and testing and come up with a suitable database model/schema
### My first thought is to design a relational database with tables as follows:

### Building:
```
class Building(db.Model):
    __tablename__ = 'buildings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_floors = db.Column(db.Integer, nullable=False)
    building_type = db.Column(db.String(50)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    elevators = db.relationship('Elevator', backref='building', lazy=True)
    
  ```

  ### This contains metadata about the building as well as a one to many relationship with the Elevator table


  ### Elevator:

```
class Elevator(db.Model):
    __tablename__ = 'elevators'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    elevator_number = db.Column(db.String(10), nullable=False)
    max_capacity = db.Column(db.Integer, default=1000)  
    current_floor = db.Column(db.Integer, default=1)
    current_load = db.Column(db.Integer, default=0) 
    is_moving = db.Column(db.Boolean, default=False)
    maintenance_status = db.Column(db.String(20), default='operational')
    last_maintenance = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    calls = db.relationship('ElevatorCall', backref='elevator', lazy=True)
```

### This table contains metadata about the elevator as well as a one to many relationship with the Elevator calls table

### Elevator Calls
```
class ElevatorCall(db.Model):
    __tablename__ = 'elevator_calls'
    
    id = db.Column(db.Integer, primary_key=True)
    elevator_id = db.Column(db.Integer, db.ForeignKey('elevators.id'), nullable=False)
    called_from_floor = db.Column(db.Integer, nullable=False)
    destination_floor = db.Column(db.Integer)
    call_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    response_time = db.Column(db.Float)  
    elevator_position_at_call = db.Column(db.Integer)  
    estimated_passengers = db.Column(db.Integer, default=1)
    call_type = db.Column(db.String(20), default='normal') 
    day_of_week = db.Column(db.Integer) 
    hour_of_day = db.Column(db.Integer)
    week_of_month = db.Column(db.Integer)
    season = db.Column(db.String(10))
    weather_condition = db.Column(db.String(20))  
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        call_dt = self.call_time or datetime.utcnow()
        self.day_of_week = call_dt.weekday()
        self.hour_of_day = call_dt.hour
        self.week_of_month = (call_dt.day - 1)
        self.season = self._get_season(call_dt.month)
    
    def _get_season(self, month: int) -> str:
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'

```

### I also created an endpoint to export training data in a suitable format for training the model, i added options for csv or json, this makes it a lot easier when working within my Notebook to have the right data.


## Evaluate the models performance

```
eval_metric=[
        'MultiClass',          
        'Accuracy',            
        'TotalF1:average=Weighted',  
        'AUC:type=MultiClass', 
        'Precision:average=Weighted',
        'Recall:average=Weighted'
    ],
```

### The CatBoost model already comes with pre-built evaluation metrics
### I would initially start with Accuracy as the base metric because it is simpler to track performance over time with statements such, the model predictions the right floor about 70% of the time, i would combine this with user satisfaction score on service delivery efficiency and quality to get a well rounded view of how the model is performing.

### This would be my process, i would keep iterating, researching until i find an approach and model that not only satifisfies the prediction target but also works well on new data and can generalize well.


## Interesting parts of this project
### Modeling how people behave with elevators is interesting, people can be unpredicatable, and simply make a decision out of feelings, maybe one day they simply dont feel like taking an elevator, for no specific reason or influence from external factors


## Challenging parts of this project

### - Network connectivity is a problem, we might need a failsafe to prevent the elevator from not working at all, 

### - What happens when unusual or sudden events occurs, like surprise inspections from  authorities at odd times or evacuations











