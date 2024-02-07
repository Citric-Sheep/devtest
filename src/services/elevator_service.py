import sqlite3
from src.services.models.elevator import Elevator
from src.services.models.demand import Demand

class ElevatorService:
    def __init__(self, db_path=":memory:"):
        self.connection = sqlite3.connect(db_path)
        self.create_elevator_table()

    def create_elevator_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elevators (
                elevator_id INTEGER PRIMARY KEY,
                current_floor INTEGER,
                resting_floor INTEGER,
                elevator_status TEXT
            )
        ''')
        self.connection.commit()

    def create_elevator(self, current_floor, resting_floor, elevator_status):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO elevators (current_floor, resting_floor, elevator_status)
            VALUES (?, ?, ?)
        ''', (current_floor, resting_floor, elevator_status))
        self.connection.commit()

        elevator_id = cursor.lastrowid
        return Elevator(elevator_id, current_floor, resting_floor, elevator_status)

    def get_elevator(self, elevator_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM elevators WHERE elevator_id = ?', (elevator_id,))
        data = cursor.fetchone()
        if data:
            return Elevator(*data)

    def update_elevator(self, elevator_id, current_floor=None, resting_floor=None, elevator_status=None):
        elevator = self.get_elevator(elevator_id)
        if elevator:
            cursor = self.connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM demands WHERE floor = ?', (elevator.current_floor,))
            demand_count = cursor.fetchone()[0]
            # Bussiness rule 1: If there are demands on the current floor, don't change elevators current floor
            if demand_count > 0 and current_floor != elevator.current_floor:
                print(f"Warning: Elevator cannot be updated to another floor due to existing demands on floor {current_floor}.")
            elif current_floor is not None:
                elevator.current_floor = current_floor
            if resting_floor is not None:
                elevator.resting_floor = resting_floor

            # Insertion of ML prediction algorithm/model for improved setup of ideal resting floor

            # Bussiness rule 2 (for now): If no new resting floor is updated, current floor shall become new resting floor.
            else: 
                elevator.resting_floor = elevator.current_floor
                print("Warning: Resting floor automatically updated, current floor shall be new resting floor.")
            if elevator_status is not None:
                elevator.elevator_status = elevator_status

            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE elevators
                SET current_floor = ?, resting_floor = ?, elevator_status = ?
                WHERE elevator_id = ?
            ''', (elevator.current_floor, elevator.resting_floor, elevator.elevator_status, elevator_id))
            self.connection.commit()

            return elevator
        else:
            print(f"Error: Elevator with ID {elevator_id} not found.")

    def delete_elevator(self, elevator_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM elevators WHERE elevator_id = ?', (elevator_id,))
        self.connection.commit()