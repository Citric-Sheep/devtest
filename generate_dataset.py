from crud_elevator import ElevatorStateManager
import random
from datetime import datetime, timedelta

elevator = ElevatorStateManager(database_url="postgresql://postgres:david.123@localhost:5432/citric_elevator")

def generate_fake_elevator_states(num_states=10, floor_number=10):
    first_floor_weight = 5
    peak_interval_multiplier = 1
    last_state = elevator.get_last_elevator_state()
    # If there is no last state, initialize randomly
    if last_state  :
        current_floor = last_state.next_floor
        demand_floor = last_state.demand_floor
        start_time = last_state.call_datetime
    else:        
        current_floor = random.choices(range(1, floor_number + 1), weights=[first_floor_weight] + [1] * (floor_number - 1))[0]
        demand_floor = random.choices(range(1, floor_number + 1), weights=[first_floor_weight] + [1] * (floor_number - 1))[0]
        start_time = datetime.today()  
    for i in range(1, num_states + 1):


        # Ensure demand_floor is different from next_floor
        while True:
            next_floor = random.choices(range(1, floor_number + 1), weights=[first_floor_weight] + [1] * (floor_number - 1))[0]
            if next_floor != demand_floor:
                break
        # Calculate time interval based on the absolute difference between next_floor and demand_floor
        # Calculate time interval based on the absolute difference between current_floor and demand_floor
   # Calculate time interval based on the absolute difference between current_floor and demand_floor
        current_floor_distance = abs(current_floor - demand_floor)
        current_floor_interval_lag = (
            10 if current_floor_distance <= 1 else min(30, current_floor_distance * 4)
        ) / 60  # Convert seconds to minutes

        # Calculate time interval based on the absolute difference between next_floor and demand_floor
        next_floor_distance = abs(next_floor - demand_floor)
        next_floor_interval_lag = (
            10 if next_floor_distance <= 1 else min(30, next_floor_distance * 4)
        ) / 60  # Convert seconds to minutes

        
        
# Introduce peak hours (for example, from 6 am to 8 am, 12 pm to 2 pm, and 5 pm to 8 pm)
        if 6 <= start_time.hour < 8 or 12 <= start_time.hour < 14 or 17 <= start_time.hour < 20:
            peak_interval_multiplier = 0.5  # Reduce time interval during peak hours

        random_minutes = random.randint(0, 5)
        interval_minutes = random_minutes*peak_interval_multiplier + current_floor_interval_lag + next_floor_interval_lag  # Time interval between states
        call_datetime = start_time + timedelta(minutes=interval_minutes)

        created_state = elevator.create_elevator_state(
            current_floor=current_floor,
            demand_floor=demand_floor,
            next_floor=next_floor,
            date_str=call_datetime.strftime("%Y-%m-%d %H:%M:%S")
        )
        print("created_state: ", created_state)

        # Update current_floor and demand_floor for the next state
        current_floor = next_floor
        demand_floor = random.choices(range(1, floor_number + 1), weights=[first_floor_weight] + [1] * (floor_number - 1))[0]
        start_time = call_datetime
generate_fake_elevator_states(num_states=10, floor_number=10)
