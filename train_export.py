"""
Example of how we could export the DB data to train an ML model.
"""

# Option 1: We can use pandas to read the SQLite DB, preprocess and export with our desired
# format, i.e. CSV, JSON, Parquet, etc.
import pandas as pd

from elevator.database import DB_PATH
from elevator.model import ElevatorDemandDb

df = pd.read_sql_table(ElevatorDemandDb.__tablename__, f"sqlite:///{DB_PATH}")
# We can extract useful data from 'requested_at' column, for example day of the week
# This could be a valuable input feature for an ML model, as some floor may request frequently
# the elevator on a certain time of a certain day of the week (i.e. Monday)
df["day_of_week"] = df["requested_at"].dt.day_name()
# Extract other features, for example:
df["is_month_start"] = df["requested_at"].dt.is_month_start.astype(int)
# Create hour and minute columns from timestamp col
df["demanded_hour"] = df["requested_at"].dt.hour
df["demanded_minute"] = df["requested_at"].dt.minute
# Keep desired cols and export
keep_cols = [
    "requested_at", "pressed_at_floor", "day_of_week", "is_month_start", "demanded_hour",
    "demanded_minute"
]
df = df.loc[df["elevator_id"] == 1, keep_cols]
df.to_csv("out.csv", index=False)

# Option 2: We could use sqlite3 command options to export to a .csv
# i.e.: sqlite3 -header -csv {DB_PATH} "select ... from elevator_demand;" > out.csv
# Inspired by this comment https://stackoverflow.com/a/21741408/4544940
# The benefit of pandas is that it can be easily exported to other formats
