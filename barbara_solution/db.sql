-- Elevator table
CREATE TABLE elevator (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,                 -- e.g., "Elevator A"
    capacity INTEGER DEFAULT 8,               -- Max passenger capacity
    is_operational BOOLEAN DEFAULT TRUE,       -- Whether it's in service
    current_floor INTEGER DEFAULT 1           -- Elevator’s last known floor
);

-- ElevatorRequest Table
CREATE TABLE elevator_request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    elevator_id INTEGER, -- Nullable if unassigned
    floor INTEGER,
    direction TEXT CHECK (direction IN ('up', 'down')) DEFAULT NULL, -- Relevant for external calls
    request_type TEXT CHECK (request_type IN ('internal', 'external')),
    FOREIGN KEY (elevator_id) REFERENCES elevator(elevator_id)
);

CREATE INDEX idx_elevator_request_timestamp
    ON elevator_request (timestamp);

-- ScheduledJob table
CREATE TABLE scheduled_job (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    elevator_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, -- Creation time
    scheduled_time DATETIME,                      -- Planned start time
    completion_time DATETIME,                     -- When it ends (optional or updated later)
    floor_arrival INTEGER,                        -- Starting floor
    floor_destination INTEGER,                    -- Ending floor
    previous_job_id INTEGER DEFAULT NULL,
    next_job_id INTEGER DEFAULT NULL,
    call_status TEXT CHECK (call_status IN ('pending', 'in_progress', 'completed', 'cancelled')) DEFAULT 'pending',
    FOREIGN KEY (elevator_id) REFERENCES elevator(id),
    FOREIGN KEY (previous_job_id) REFERENCES scheduled_job(id),
    FOREIGN KEY (next_job_id) REFERENCES scheduled_job(id)
);

-- Linking Table for Requests and Jobs
CREATE TABLE job_request_link (
    job_id INTEGER,
    request_id INTEGER,
    PRIMARY KEY (job_id, request_id),
    FOREIGN KEY (job_id) REFERENCES scheduled_job(id),
    FOREIGN KEY (request_id) REFERENCES elevator_request(id)
);

-- ElevatorDailyMetrics table
CREATE TABLE elevator_daily_metrics (
    elevator_id INTEGER PRIMARY KEY,
    capacity INTEGER,
    is_operational BOOLEAN DEFAULT TRUE,
    total_trips INTEGER DEFAULT 0,
    total_distance INTEGER DEFAULT 0,
    max_weight_occupancy INTEGER,
    energy_consumption REAL DEFAULT 0.0,
    time_idle INTEGER DEFAULT 0,
    time_moving INTEGER DEFAULT 0,
    FOREIGN KEY (elevator_id) REFERENCES elevator(id)
);

-- Floors table
CREATE TABLE floors (
    floor_id INTEGER PRIMARY KEY,
    floor_number INTEGER UNIQUE,
    is_accessible BOOLEAN DEFAULT TRUE
);

-- Indexes for performance
CREATE INDEX idx_elevator_request_timestamp
    ON elevator_request (timestamp);

CREATE INDEX idx_scheduled_job_prev_next
    ON scheduled_job (previous_job_id, next_job_id);