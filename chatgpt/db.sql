-- Create table to storage all the demands of the elevator --
CREATE TABLE elevator_demands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    floor INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    hour_of_day INTEGER NOT NULL,
);

-- Create table to storage the states of the elevator --
CREATE TABLE elevator_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    floor INTEGER NOT NULL,
    vacant BOOLEAN NOT NULL,
    day_of_week INTEGER NOT NULL,
    hour_of_day INTEGER NOT NULL,
    demand_id INTEGER,
    FOREIGN KEY (demand_id) REFERENCES elevator_demands(id)
);

-- Indexes to optimize frequent queries --
-- Note: These indexes are not actively used in the current API endpoints,
-- but are included to support future machine learning tasks that may require
-- efficient filtering or grouping by timestamp or floor --
CREATE INDEX idx_demands_timestamp ON elevator_demands(timestamp);
CREATE INDEX idx_states_timestamp ON elevator_states(timestamp);
CREATE INDEX idx_demands_floor ON elevator_demands(floor);
CREATE INDEX idx_states_floor ON elevator_states(floor);