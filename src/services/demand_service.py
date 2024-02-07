import sqlite3
from datetime import datetime
from src.services.models.demand import Demand

class DemandService:
    def __init__(self, db_path:str=":memory:"):
        """
        Initialize the DemandService with the path to the SQLite database.

        Parameters:
        - db_path (str): Path to the SQLite database file. Default is ":memory:" for in-memory database.
        """
        self.connection = sqlite3.connect(db_path)
        self.create_demand_table()

    def create_demand_table(self):
        """
        Create the demands table in the SQLite database if it doesn't exist.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS demands (
                demand_id INTEGER PRIMARY KEY,
                floor INTEGER,
                timestamp DATETIME
            )
        ''')
        self.connection.commit()

    def create_demand(self, floor:int, timestamp:datetime):
        """
        Create a new demand entry in the database.

        Parameters:
        - floor (int): The floor number where the demand is made.
        - timestamp (datetime): The timestamp of the demand in "YYYY-MM-DD HH:MM:SS" format.

        Returns:
        - Demand: The Demand object representing the newly created demand.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO demands (floor, timestamp)
            VALUES (?, ?)
        ''', (floor, timestamp))
        self.connection.commit()

        demand_id = cursor.lastrowid
        return Demand(demand_id, floor, timestamp)
        
    def get_demand(self, demand_id:int):
        """
        Retrieve a demand entry from the database by its ID.

        Parameters:
        - demand_id (int): The ID of the demand to retrieve.

        Returns:
        - Demand or None: The Demand object if found, None otherwise.
        """
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM demands WHERE demand_id = ?', (demand_id,))
        data = cursor.fetchone()
        if data:
            demand = Demand(*data)
            demand.timestamp = datetime.strptime(data[2], "%Y-%m-%d %H:%M:%S")
            return demand

    def delete_demand(self, demand_id:int):
        """
        Delete a demand entry from the database by its ID.

        Parameters:
        - demand_id (int): The ID of the demand to delete.
        """
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM demands WHERE demand_id = ?', (demand_id,))
        self.connection.commit()
