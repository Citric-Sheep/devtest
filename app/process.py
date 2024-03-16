from models import Demand, ElevatorMovement
from sqlalchemy import func
import pandas as pd

class FloorData:
    def __init__(self, floor, stops=None, demand=None):
        self.floor = floor
        self.stops = stops
        self.demand = demand

def preprocessing(min_stops):
    # Retrieve all elevator movements and demands from the database
    elevator_movements = ElevatorMovement.query.all()
    demands = Demand.query.all()

    # Convert retrieved data into Pandas DataFrames
    elevator_movements_df = pd.DataFrame([movement.serialize() for movement in elevator_movements])
    demands_df = pd.DataFrame([demand.serialize() for demand in demands])

    # Calculate the number of stops per floor and demand per floor
    stops_per_floor = elevator_movements_df.groupby('next_floor').size().reset_index(name='stops')
    demand_per_floor = demands_df.groupby('floor').size().reset_index(name='demand')

    # Merge the DataFrames to combine stops and demand data
    merged_df = pd.merge(stops_per_floor, demand_per_floor, how='outer', left_on='next_floor', right_on='floor')

    # Filter floors with a minimum number of stops
    min_stops = int(min_stops)
    filtered_df = merged_df[merged_df['stops'] >= min_stops]

    # Create FloorData objects for filtered data
    floor_data = [FloorData(floor=row['next_floor'], stops=row['stops'], demand=row['demand']) for _, row in filtered_df.iterrows()]

    # Return the processed floor data
    return floor_data

