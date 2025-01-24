CREATE TABLE state (
    state_id INTEGER PRIMARY KEY AUTOINCREMENT,  
    current_floor INTEGER NOT NULL,              -- Current floor the elevator is on
    vacant BOOLEAN NOT NULL,                     -- Status indicating if the elevator is vacant (TRUE = vacant, FALSE = occupied)
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP -- Timestamp when the state is recorded
);

CREATE TABLE demand (
    demand_id INTEGER PRIMARY KEY AUTOINCREMENT,  
    state_id INTEGER,                             -- Foreign Key linking to the state table
    demand_floor INTEGER NOT NULL,                -- Floor where the demand originated (the floor from which the elevator is called)
    direction INTEGER NOT NULL,                   -- Direction of the elevator (1 = up, 0 = down)
    season INTEGER,                               -- Quarter of the year (1 = Q1, 2 = Q2, 3 = Q3, 4 = Q4)
    month_number INTEGER,                                -- Month of the year (1 = January, 12 = December)
    day_of_week INTEGER,                          -- Day of the week (1 = Monday, 7 = Sunday)
    time_of_day INTEGER,                          -- Time of the day (1 = morning, 2 = afternoon, 3 = evening, 4 = overnight)
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP -- Timestamp when the demand is logged
    FOREIGN KEY(state_id) REFERENCES state(state_id)
);
