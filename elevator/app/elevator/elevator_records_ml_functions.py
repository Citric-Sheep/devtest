import csv

from db import elevator
from datetime import timedelta


def get_records_by_elevator_id_with_resting_floor_calculated(elevator_id):
    elevator_records = elevator.get_records_by_elevator_id(elevator_id)

    resting_floor_widows_of_time_records = []

    for i in range(len(elevator_records) - 1):
        if elevator_records[i]["movement_type"] == "":
            time_difference = elevator_records[i + 1]["demand_time"] - elevator_records[i]["demand_time"]
            seconds_difference = time_difference.total_seconds()

            for j in range(1, int(seconds_difference)):
                resting_floor_record = elevator_records[i].copy()
                resting_floor_record["demand_time"] += timedelta(seconds=j)
                resting_floor_record["arrival_time"] += timedelta(seconds=j)
                resting_floor_widows_of_time_records.append(resting_floor_record)

    elevator_records.extend(resting_floor_widows_of_time_records)
    elevator_records.sort(key=lambda x: x['demand_time'])

    for elevator_record in elevator_records:
        elevator_record['resting_floor'] = 1 if elevator_record['movement_type'] == "" else 0
        # To be serializable
        elevator_record['demand_time'] = elevator_record['demand_time'].strftime('%Y-%m-%d %H:%M:%S')
        elevator_record['arrival_time'] = elevator_record['arrival_time'].strftime('%Y-%m-%d %H:%M:%S')

    # column_names = list(elevator_records[0].keys())S

    # file_name = 'training_data.csv'
    #
    # with open(file_name, 'w', newline='') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=column_names)
    #     writer.writeheader()
    #     writer.writerows(elevator_records)

    return elevator_records
