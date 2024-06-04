import sqlite3

# Connect to the SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('test.db')

# Read the DDL commands from the file
with open('ddl.sql', 'r') as file:
    ddl_script = file.read()

# Execute the DDL script
with conn:
    conn.executescript(ddl_script)

print("Database initialized successfully.")
