import random
import datetime
import requests


def init_timeline(start_time, end_time, time_step):
    #Initialize stamps list
    time_stamps = []
    current_time = start_time
    while current_time <= end_time:
        time_stamps.append(current_time)
        current_time += time_step

    return time_stamps

def random_time_stamps(time_stamps, k):
    #Pick random time stamps from the complete timeline
    n = len(time_stamps)
    weights = [(0.2 if dt.hour in [6,7,12,13,17,18] else 0.1) for dt in time_stamps]    #Take into account peak hours

    return random.choices(time_stamps, weights=weights, k=min(k,n))

def call_elevator(dt, n):
    #Extracts data from an elevator call. The future next floor elevator call is assumpted 
    week_day = dt.strftime('%A')
    hour = dt.hour
    source = random.randint(1,n)
    target = random.randint(1,n)
    while source==target:
        target = random.randint(1,n)
    capacity = random.randint(4,8)
    occupancy = random.randint(1,capacity)
    next_floor = random.randint(1,n)

    return {"week_day":week_day, "hour":hour, "requested_floor":source, "target_floor":target, "capacity":capacity, "occupancy":occupancy, "next_floor":next_floor}


def simulate(start_time, end_time, n_floors):
    #Creates a list of random elevator events
    time_stamps = random_time_stamps(init_timeline(start_time, end_time, datetime.timedelta(minutes=1)), 5000)
    sim = []

    for ts in time_stamps:
        sim.append(call_elevator(ts, n_floors))


    return sim



