import sqlite3
from src.services.models.elevator import Elevator
from src.services.models.demand import Demand

class ElevatorService:
    def __init__(self, db_path:str=":memory:"):
        """
        Initialize the ElevatorService with the path to the SQLite database.

        Parameters:
        - db_path (str): Path to the SQLite database file. Default is ":memory:" for in-memory database.
        """
        self.connection = sqlite3.connect(db_path)
        self.create_elevator_table()

    def create_elevator_table(self):
        """
        Create the elevators table in the SQLite database if it doesn't exist.
        """
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

    def create_elevator(self, current_floor:int, resting_floor:int, elevator_status:str):
        """
        Create a new elevator entry in the database.

        Parameters:
        - current_floor (int): The current floor where the elevator is located.
        - resting_floor (int): The resting floor for the elevator when it's not in use.
        - elevator_status (str): The status of the elevator (e.g., "Idle", "Moving").

        Returns:
        - Elevator: The Elevator object representing the newly created elevator.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO elevators (current_floor, resting_floor, elevator_status)
            VALUES (?, ?, ?)
        ''', (current_floor, resting_floor, elevator_status))
        self.connection.commit()

        elevator_id = cursor.lastrowid
        return Elevator(elevator_id, current_floor, resting_floor, elevator_status)

    def get_elevator(self, elevator_id:int):
        """
        Retrieve an elevator entry from the database by its ID.

        Parameters:
        - elevator_id (int): The ID of the elevator to retrieve.

        Returns:
        - Elevator or None: The Elevator object if found, None otherwise.
        """
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM elevators WHERE elevator_id = ?', (elevator_id,))
        data = cursor.fetchone()
        if data:
            return Elevator(*data)

    def update_elevator(self, elevator_id:int, current_floor:int=None, resting_floor:int=None, elevator_status:str=None):
        elevator = self.get_elevator(elevator_id)
        """
        Update an elevator entry in the database by its ID.

        Parameters:
        - elevator_id (int): The ID of the elevator to update.
        - current_floor (int): The new current floor of the elevator (optional).
        - resting_floor (int): The new resting floor of the elevator (optional).
        - elevator_status (str): The new status of the elevator (optional).

        Returns:
        - Elevator or None: The updated Elevator object if successful, None if the elevator ID is not found.
        """
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

    def delete_elevator(self, elevator_id:int):
        """
        Delete an elevator entry from the database by its ID.

        Parameters:
        - elevator_id (int): The ID of the elevator to delete.
        """
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM elevators WHERE elevator_id = ?', (elevator_id,))
        self.connection.commit()