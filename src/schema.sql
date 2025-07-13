-- Elevator system database schema

-- Building information
CREATE TABLE buildings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    floors INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Elevator information
CREATE TABLE elevators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (building_id) REFERENCES buildings(id)
);

-- Elevator calls (demands)
CREATE TABLE elevator_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    elevator_id INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    floor INTEGER NOT NULL,
    direction TEXT CHECK(direction IN ('up', 'down')) NOT NULL,
    wait_time INTEGER,  -- Time in seconds until elevator arrived
    FOREIGN KEY (elevator_id) REFERENCES elevators(id)
);

-- Elevator trips
CREATE TABLE elevator_trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    elevator_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    origin_floor INTEGER NOT NULL,
    destination_floor INTEGER NOT NULL,
    occupancy BOOLEAN NOT NULL,  -- TRUE if elevator had passengers
    FOREIGN KEY (elevator_id) REFERENCES elevators(id)
);

-- Elevator states (captures point-in-time state)
CREATE TABLE elevator_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    elevator_id INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    floor INTEGER NOT NULL,
    is_vacant BOOLEAN NOT NULL,
    is_moving BOOLEAN NOT NULL,
    is_resting BOOLEAN GENERATED ALWAYS AS (is_vacant AND NOT is_moving) STORED,
    FOREIGN KEY (elevator_id) REFERENCES elevators(id)
);

-- Time-based statistics (for ML features)
CREATE TABLE time_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    elevator_id INTEGER NOT NULL,
    date DATE NOT NULL,
    hour INTEGER NOT NULL CHECK(hour BETWEEN 0 AND 23),
    calls_count INTEGER DEFAULT 0,
    most_common_origin_floor INTEGER,
    most_common_destination_floor INTEGER,
    FOREIGN KEY (elevator_id) REFERENCES elevators(id),
    UNIQUE(elevator_id, date, hour)
);

-- Floor-based statistics (for ML features)
CREATE TABLE floor_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    elevator_id INTEGER NOT NULL,
    floor INTEGER NOT NULL,
    date DATE NOT NULL,
    calls_count INTEGER DEFAULT 0,
    avg_wait_time REAL,
    FOREIGN KEY (elevator_id) REFERENCES elevators(id),
    UNIQUE(elevator_id, floor, date)
);

-- Indexes for performance
CREATE INDEX idx_elevator_calls_timestamp ON elevator_calls(timestamp);
CREATE INDEX idx_elevator_states_timestamp ON elevator_states(timestamp);
CREATE INDEX idx_elevator_trips_start_time ON elevator_trips(start_time);
CREATE INDEX idx_time_statistics_date_hour ON time_statistics(date, hour);
CREATE INDEX idx_floor_statistics_floor_date ON floor_statistics(floor, date);