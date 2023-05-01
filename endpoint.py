from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)
DATABASE = 'elevator_events.db'

# Create the SQLite database and table if don't exists
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS elevator_events (
                  id INTEGER PRIMARY KEY,
                  week_day TEXT NOT NULL,
                  hour INTEGER NOT NULL,
                  requested_floor INTEGER NOT NULL,
                  target_floor INTEGER NOT NULL,
                  capacity INTEGER NOT NULL,
                  occupancy INTEGER NOT NULL,
                  next_floor INTEGER NOT NULL
                  )''')
conn.close()


#Data enpoint
@app.route('/elevator-request', methods=['POST'])
def elevator_request():
    content = request.json
    week_day = content['week_day']
    hour = int(content['hour'])
    requested_floor = int(content['requested_floor'])
    target_floor = int(content['target_floor'])
    capacity = int(content['capacity'])
    occupancy = int(content['occupancy'])
    next_floor = int(content['next_floor'])

    # Insert the data into the events table
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO elevator_events (week_day, hour, requested_floor, target_floor, capacity, occupancy, next_floor) VALUES (?, ?, ?, ?, ?, ?, ?)', (week_day, hour, requested_floor, target_floor, capacity, occupancy, next_floor))
    conn.commit()
    conn.close()

    return "Nice!"

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True, port=8020)