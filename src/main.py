import argparse
from simulator import run
from parameters.utils import generate_lambda_table
from datetime import datetime


# SIMULATION PARAMETERS
# number of floors in the building
FLOORS = 10
# simulation start datetime
START_DATETIME = datetime(2024, 4, 1, 0, 0)
# simulation end datetime
END_DATETIME = datetime(2024, 4, 30, 23, 59)
# simulation steps unit (also interval for Poisson distribution)
TIME_UNIT_IN_MINUTES = 5
# Poisson distribution parameters: one per (day of week, hour) combination
# generated randomly: you could set it manually if you have this information
LAMBDAS = generate_lambda_table(min_lambda=0.0, max_lambda=5.0)


def main() -> None:
    # parse arguments
    parser = argparse.ArgumentParser(description="Run elevator simulator")
    parser.add_argument("--reset", action="store_true", help="Reset the database")
    args = parser.parse_args()

    # run simulation
    run(
        floors=FLOORS,
        lambdas=LAMBDAS,
        start_datetime=START_DATETIME,
        end_datetime=END_DATETIME,
        time_unit_in_minutes=TIME_UNIT_IN_MINUTES,
        reset=args.reset
    )


if __name__ == "__main__":
    main()
