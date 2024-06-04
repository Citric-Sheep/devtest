CREATE TABLE IF NOT EXISTS Floors (
    floor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    floor_number INTEGER NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ElevatorEvents (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    source_floor_id INTEGER,
    destination_floor_id INTEGER,
    num_persons INTEGER,
    weight FLOAT,
    event_type TEXT NOT NULL,
    FOREIGN KEY (source_floor_id) REFERENCES Floors(floor_id),
    FOREIGN KEY (destination_floor_id) REFERENCES Floors(floor_id)
);
