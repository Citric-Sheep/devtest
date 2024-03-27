
"""-- Crear la tabla de viajes del ascensor
CREATE TABLE IF NOT EXISTS ElevatorTrips (
    TripID INTEGER PRIMARY KEY AUTOINCREMENT,
    StartFloor INTEGER NOT NULL,
    EndFloor INTEGER NOT NULL,
    StartTime DATETIME NOT NULL,
    EndTime DATETIME NOT NULL,
    IsDemand BOOLEAN NOT NULL
);

-- Crear la tabla de estado del ascensor
CREATE TABLE IF NOT EXISTS ElevatorStatus (
    StatusID INTEGER PRIMARY KEY AUTOINCREMENT,
    CurrentFloor INTEGER NOT NULL,
    IsMoving BOOLEAN NOT NULL,
    Timestamp DATETIME NOT NULL
);"""