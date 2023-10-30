import sqlite3
import datetime
import random
import numpy as np

con = sqlite3.connect("database.db")
cur = con.cursor()

create_table = """ 
    CREATE TABLE IF NOT EXISTS elevator (
        id INTEGER PRIMARY KEY,
        calling_floor INTEGER,
        resting_floor INTEGER,
        time TIMESTAMP,
        time_block INTEGER
    );
"""

cur.execute(create_table)

numberOfFloors = 20
numberOfDays = 365

floors = [i for i in range(1,numberOfFloors+1)]

numOfcallsIdeal  = 100000

floorMostCallings = 6
idealRestingFloor = 15

pcalling = np.array([ 10000*np.random.random() if i!=floorMostCallings else numOfcallsIdeal for i in range(1,numberOfFloors+1)])
pcalling = pcalling/pcalling.sum()


presting = np.array([ 10000*np.random.random() if i!=idealRestingFloor else numOfcallsIdeal for i in range(1,numberOfFloors+1)])
presting = presting/presting.sum()


resting_floor = random.choice(floors)
print(f"Running ... ")

number_of_calls = 0

for day in range(numberOfDays):
    
    print(f"Day {day + 1}")
    for hh in range(24):
        
        start_min = random.choice(range(1,58))
        jump = random.choice([1,2,3,4,5,6,7,8,9,10])
        
        for mm in range(start_min,60,jump):
            
            ss =  random.choice(range(1,58)) 
            current_time = day + hh + mm/60
            calling_floor = np.random.choice(floors,p=pcalling)
            
            while calling_floor == resting_floor:
                calling_floor = np.random.choice(floors,p=pcalling)
            
            row = (int(calling_floor), int(resting_floor), datetime.time(hh,mm,ss).strftime("%H:%M:%S"),hh)
            cur.execute("INSERT INTO elevator (calling_floor,resting_floor,time,time_block) VALUES(?,?,?,?)", row)
            resting_floor = np.random.choice(floors,p=presting)
                
            number_of_calls += 1

            con.commit()
        
con.close()

print("Data generated!")