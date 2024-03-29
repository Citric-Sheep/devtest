import sqlite3
import sys
import csv
sys.path.append('..')
from src.constants import DAYS_OF_THE_WEEK
from .utils import datetime_to_integer
from datetime import datetime


class ElevatorDatabase:
    def __init__(self, db_name: str) -> None:
        """
        Initialize the ElevatorDatabase instance.

        Args:
            db_name (str): The name of the database to connect to.
        """
        self.connector = None
        self.cursor = None
        self.db_name = db_name
        self._connect()
        self._create_tables()


    def _connect(self) -> None:
        """
        Connect to the SQLite database.

        """
        self.connector = sqlite3.connect(self.db_name)
        self.cursor = self.connector.cursor()


    def _create_tables(self) -> None:
        """
        Create the 'call' table in the database if it doesn't exist.

        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS call(
                day_of_week INTEGER,
                time INTEGER,
                source_floor INTEGER,
                destination_floor INTEGER
            )
            """
        )
        self.connector.commit()


    def _insert(self, data: list[tuple[int, int, int, int]]) -> None:
        """
        Insert multiple records into the 'call' table.

        Args:
            data (list[tuple[int, int, int, int]]): A list of tuples, where each tuple contains four integers representing
            day_of_week, time, source_floor, and destination_floor respectively.
        """
        self.cursor.executemany(
            "INSERT INTO call VALUES (?, ?, ?, ?)",
            data
        )
        self.connector.commit()


    def push(self, calls: dict[str, int], day_of_week: str, dt: datetime) -> None:
        """
        Push call data into the database.

        Args:
            calls (dict[str, int]): A dictionary containing call information, where each call has keys "source_floor" and "destination_floor".
            day_of_week (str): The day of the week for the calls.
            dt (datetime): The datetime object representing the time of the calls.
        """
        dow = DAYS_OF_THE_WEEK.index(day_of_week) + 1
        time = datetime_to_integer(dt)
        data = [
            (dow, time, call["source_floor"], call["destination_floor"])
            for call in calls
        ]
        self._insert(data)


    def export(self, filename: str = "calls.csv") -> None:
        """
        Export call data from the database to a CSV file.

        Args:
            filename (str, optional): The name of the CSV file to export data to. Defaults to "calls.csv".
        """
        with open(filename, 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([
                "Day_of_week",
                "Time",
                "Source_floor",
                "Destination_floor"
            ])
            self.cursor.execute("SELECT * FROM call")
            rows = self.cursor.fetchall()
            csv_writer.writerows(rows)


    def reset(self) -> None:
        """
        Reset the database by dropping and recreating the 'call' table.

        """
        self.cursor.execute("DROP TABLE IF EXISTS call")
        self._create_tables()


    def close(self) -> None:
        """
        Close the connection to the database.

        """
        self.connector.close()
