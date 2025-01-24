import sqlite3
import datetime

DB_FILE = "elevator.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def get_time_of_day():
    now = datetime.datetime.now()
    if 6 <= now.hour < 12:
        return 1  # morning
    elif 12 <= now.hour < 18:
        return 2  # afternoon
    elif 18 <= now.hour < 24:
        return 3  # evening
    else:
        return 4  # overnight

def get_season(month_number):
    if 1 <= month_number <= 3:
        return 1  # Q1
    elif 4 <= month_number <= 6:
        return 2  # Q2
    elif 7 <= month_number <= 9:
        return 3  # Q3
    else:
        return 4  # Q4

def log_demand(demand_floor, direction):
    now = datetime.datetime.now()
    month_number = now.month  # Get current month number (1 - 12)
    day_of_week = now.weekday() + 1  # Get current day of the week (1 = Monday, 7 = Sunday)
    time_of_day = get_time_of_day()
    season = get_season(month_number)  # Calculate season based on month

    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve the current state (assuming the state is being logged)
    cursor.execute("SELECT state_id FROM state WHERE vacant = 1")  # Find an available (vacant) elevator
    state = cursor.fetchone()

    if state:
        state_id = state[0]
        cursor.execute(
            """
            INSERT INTO demand (state_id, demand_floor, direction, season, month_number, day_of_week, time_of_day)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (state_id, demand_floor, direction, season, month_number, day_of_week, time_of_day)
        )
        conn.commit()
    else:
        print("No vacant elevator found for the demand")
    
    conn.close()

def get_feature_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT s.state_id, s.vacant, s.current_floor, d.demand_floor, d.direction, d.season, d.month_number, 
               d.day_of_week, d.time_of_day
        FROM state s
        JOIN demand d ON s.state_id = d.state_id
        """
    )
    demand_data = cursor.fetchall()
    conn.close()
    return [
        {"state_id": row[0], "vacant": row[1], "current_floor": row[2], "demand_floor": row[3], 
         "direction": row[4], "season": row[5], "month_number": row[6], "day_of_week": row[7], "time_of_day": row[8]}
        for row in demand_data
    ]