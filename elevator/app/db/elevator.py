from .connection import DataBase

db = DataBase()
cursor = db.conn.cursor()
DB_NAME = 'elevator_db'


def create_database():   
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    db.conn.commit()


def create_elevator_tables():
    print("Creating tables")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS elevators (
            id INT AUTO_INCREMENT PRIMARY KEY,
            lower_floor INT,
            top_floor INT,
            last_record_id INT,
            is_up BOOLEAN,
            is_vacant BOOLEAN,
            is_on_demand BOOLEAN
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS elevator_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            elevator_id INT,
            FOREIGN KEY (elevator_id) REFERENCES elevators(id),
            current_floor INT,
            target_floor INT,
            direction INT,
            movement_type VARCHAR(20),
            demand_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            arrival_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_vacant BOOLEAN
        )""")

    db.conn.commit()


def create_elevator(top_floor=10, lower_floor=-1, last_record_id=0, is_up=False, is_vacant=True, is_on_demand=False):
    cursor.execute(f"""
        INSERT INTO elevators (
            top_floor,
            lower_floor,
            last_record_id,
            is_up,
            is_vacant,
            is_on_demand
    ) VALUES (
            {top_floor}, 
            {lower_floor}, 
            {last_record_id}, 
            {is_up}, 
            {is_vacant},
            {is_on_demand})
    """)
    print("Elevator created in db")
    elevator_id = cursor.lastrowid
    db.conn.commit()
    return elevator_id


def get_elevator_by_id(elevator_id):
    cursor.execute(f"SELECT * FROM {DB_NAME}.elevators WHERE id = {elevator_id}")
    elevator_values = cursor.fetchone()
    if elevator_values:
        elevator_keys = cursor.column_names
        elevator_dict = dict(zip(elevator_keys, elevator_values))
        return elevator_dict
    return {}


def update_elevator(elevator_id, last_record_id=None, is_up=None, is_vacant=None, is_on_demand=None):
    set_clauses = []

    if last_record_id is not None:
        set_clauses.append(f"last_record_id = {last_record_id}")
    if is_up is not None:
        set_clauses.append(f"is_up = {is_up}")
    if is_vacant is not None:
        set_clauses.append(f"is_vacant = {is_vacant}")
    if is_on_demand is not None:
        set_clauses.append(f"is_on_demand = {is_on_demand}")

    set_clause_str = ",\n".join(set_clauses)

    query = f"""
        UPDATE {DB_NAME}.elevators
        SET 
            {set_clause_str}
        WHERE
            id = {elevator_id}
    """
    cursor.execute(query)
    db.conn.commit()
    return elevator_id


def create_elevator_record(elevator_id, current_floor=1, target_floor=1, direction=0, movement_type="", demand_time=None,
                           arrival_time=None, is_vacant=True):
    cursor.execute(f"""
        INSERT INTO elevator_records (
            elevator_id,
            current_floor,
            target_floor,
            direction,
            movement_type,
            {'demand_time,' if demand_time else ''}
            {'arrival_time,' if arrival_time else ''}
            is_vacant
        ) VALUES (
            {elevator_id}, 
            {current_floor}, 
            {target_floor}, 
            {direction},
            "{movement_type}",
            {f"'{demand_time}'," if demand_time else ""}
            {f"'{arrival_time}'," if arrival_time else ""}
            {is_vacant});
    """)

    record_id = cursor.lastrowid
    # Commit changes and close connection
    db.conn.commit()
    return record_id


def get_elevator_record_with_higher_timestamp_by_elevator_id(elevator_id):
    cursor.execute(f"""SELECT elevator_id, arrival_time as elevator_last_trip_timestamp
        FROM elevator_records 
        WHERE elevator_id = {elevator_id}
        ORDER BY arrival_time DESC
        LIMIT 1;""")
    elevator_last_trip_values = cursor.fetchone()
    if elevator_last_trip_values:
        elevator_last_trip_keys = cursor.column_names
        elevator_last_trip_dict = dict(zip(elevator_last_trip_keys, elevator_last_trip_values))
        return elevator_last_trip_dict
    return {}


def get_record_by_id(elevator_record_id):
    cursor.execute(f"SELECT * FROM {DB_NAME}.elevator_records WHERE id = {elevator_record_id}")
    elevator_record_values = cursor.fetchone()
    if elevator_record_values:
        elevator_record_keys = cursor.column_names
        elevator_record_dict = dict(zip(elevator_record_keys, elevator_record_values))
        return elevator_record_dict
    return {}


def get_records_by_elevator_id(elevator_id):
    cursor.execute(f"SELECT * FROM elevator_db.elevator_records WHERE elevator_id = {elevator_id}")
    elevator_records_values = cursor.fetchall()
    elevator_record_keys = cursor.column_names
    elevator_records = []
    if elevator_records_values:
        for elevator_record_values in elevator_records_values:
            if elevator_record_values:
                elevator_records.append(dict(zip(elevator_record_keys, elevator_record_values)))
        return elevator_records
    return []

