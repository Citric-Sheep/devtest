import os
import sqlite3

if os.path.exists("elevator_system.db"):
    os.remove("elevator_system.db")
    print("Previous database deleted.")

conn = sqlite3.connect("elevator_system.db")
cursor = conn.cursor()

with open("src/schema.sql", "r") as f:
    schema = f.read()

cursor.executescript(schema)
conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Created tables:")
for table in tables:
    print(f"- {table[0]}")

conn.close()

print("Database initialized successfully.")