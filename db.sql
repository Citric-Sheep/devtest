CREATE TABLE your_table_name (
    entry_id SERIAL PRIMARY KEY,
    cur_position NUMERIC NOT NULL,
    time_stamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    demanded INTEGER NOT NULL
);

CREATE FUNCTION public.check_elevator_moved()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST null
    VOLATILE NOT LEAKPROOF
AS $BODY$
DECLARE
  prev_position INTEGER;
BEGIN
  SELECT cur_position INTO prev_position
  FROM elevator_registry
  WHERE entry_id < NEW.entry_id
  ORDER BY time_stamp DESC
  LIMIT 1;

  IF NEW.demanded = 1 AND NEW.cur_position = prev_position THEN
    RAISE EXCEPTION 'Cannot call the elevator (called_by_passenger = 1) without changing the floor';
  END IF;

  RETURN NEW;
END;
$BODY$;

ALTER FUNCTION public.check_elevator_moved()
    OWNER TO postgres;

COMMENT ON FUNCTION public.check_elevator_moved()
    IS 'null';

INSERT INTO elevator_positions (position, timestamp, called_by_passenger)
VALUES
  (5, '2023-09-07 10:15:00', 1),  -- Elevator called to the 5th floor
  (0, '2023-09-07 10:30:00', 0),  -- Elevator moved to the 0th floor by passenger
  (0, '2023-09-07 10:35:00', 0),  -- Elevator still at the 0th floor
  (0, '2023-09-07 10:40:00', 0),  -- Elevator still at the 0th floor
  (0, '2023-09-07 10:45:00', 0),  -- Elevator still at the 0th floor
  (0, '2023-09-07 10:50:00', 0),  -- Elevator still at the 0th floor
  (2, '2023-09-07 11:30:45', 0),  -- Passenger moved the elevator to the 2nd floor
  (2, '2023-09-07 11:35:00', 0),  -- Elevator still at the 2nd floor
  (2, '2023-09-07 11:40:00', 0),  -- Elevator still at the 2nd floor
  (8, '2023-09-07 13:45:20', 1);  -- Elevator called to the 8th floor
