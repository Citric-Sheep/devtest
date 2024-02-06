import sqlite3
from datetime import datetime
from src.services.models.demand import Demand

class DemandService:
    def __init__(self, db_path=":memory:"):
        self.connection = sqlite3.connect(db_path)
        self.create_demand_table()

    def create_demand_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS demands (
                demand_id INTEGER PRIMARY KEY,
                floor INTEGER,
                timestamp DATETIME
            )
        ''')
        self.connection.commit()

    def create_demand(self, floor, timestamp):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO demands (floor, timestamp)
            VALUES (?, ?)
        ''', (floor, timestamp))
        self.connection.commit()

        demand_id = cursor.lastrowid
        return Demand(demand_id, floor, timestamp)
        
    def get_demand(self, demand_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM demands WHERE demand_id = ?', (demand_id,))
        data = cursor.fetchone()
        if data:
            demand = Demand(*data)
            demand.timestamp = datetime.strptime(data[2], "%Y-%m-%d %H:%M:%S")
            return demand

    def delete_demand(self, demand_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM demands WHERE demand_id = ?', (demand_id,))
        self.connection.commit()
