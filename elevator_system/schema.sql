-- Elevator Prediction System Database Schema
-- Single table design focused on the "Golden Event" for ML training

CREATE TABLE demand_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_rested DATETIME NOT NULL,      -- When elevator became idle
    timestamp_called DATETIME NOT NULL,      -- When next call was received
    resting_floor INTEGER NOT NULL,          -- Floor elevator was resting on
    call_floor INTEGER NOT NULL,             -- Floor the call came from
    destination_floor INTEGER,               -- Where user wants to go
    day_of_week INTEGER NOT NULL,            -- 0-6 (Monday-Sunday)
    hour_of_day INTEGER NOT NULL             -- 0-23
);

-- Create indexes for better query performance
CREATE INDEX idx_demand_log_timestamp_rested ON demand_log(timestamp_rested);
CREATE INDEX idx_demand_log_timestamp_called ON demand_log(timestamp_called);
CREATE INDEX idx_demand_log_resting_floor ON demand_log(resting_floor);
CREATE INDEX idx_demand_log_call_floor ON demand_log(call_floor);
CREATE INDEX idx_demand_log_time_features ON demand_log(day_of_week, hour_of_day);

-- Example queries for ML data extraction:

-- 1. Get all training data (features and labels)
SELECT 
    resting_floor,
    day_of_week,
    hour_of_day,
    destination_floor,
    call_floor as label
FROM demand_log
ORDER BY timestamp_called DESC;

-- 2. Find most common call floor for each resting floor
SELECT 
    resting_floor,
    call_floor,
    COUNT(*) as frequency
FROM demand_log 
GROUP BY resting_floor, call_floor
ORDER BY resting_floor, frequency DESC;

-- 3. Analyze time patterns
SELECT 
    day_of_week,
    hour_of_day,
    call_floor,
    COUNT(*) as call_count
FROM demand_log 
GROUP BY day_of_week, hour_of_day, call_floor
ORDER BY day_of_week, hour_of_day, call_count DESC;

-- 4. Calculate idle time statistics
SELECT 
    resting_floor,
    AVG((julianday(timestamp_called) - julianday(timestamp_rested)) * 24 * 60) as avg_idle_minutes,
    COUNT(*) as total_events
FROM demand_log 
GROUP BY resting_floor
ORDER BY avg_idle_minutes DESC;