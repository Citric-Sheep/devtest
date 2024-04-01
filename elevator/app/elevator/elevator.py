from db import elevator
from datetime import datetime, timedelta

RESTING_DIRECTION = 0
RESTING_FLOOR_IS_VACANT_VALUE = True


class Elevator:
    
    def __init__(self):
        self.current_floor = 1
        self.elevator_floor = 1
        self.current_elevator_id = 0
        self.top_floor = 10
        self.lower_floor = -1 
        self.last_record_id = 0
        self.is_up = False
        self.is_vacant = True
        self.is_on_demand = False
        self.elevator_page_args = {}

    def create_elevator(self, top_floor, lower_floor, set_as_default=False):
        print("I'm trying to create an elevator")
        elevator_id = elevator.create_elevator(top_floor=top_floor, lower_floor=lower_floor)
        record_id = elevator.create_elevator_record(elevator_id=elevator_id)
        if set_as_default:
            self.current_elevator_id = elevator_id
            self.top_floor = top_floor
            self.lower_floor = lower_floor
            self.last_record_id = record_id

            elevator.update_elevator(
                elevator_id=elevator_id,
                last_record_id=record_id)

        return elevator_id

    # TODO: Get elevator, to chose one of them
    @staticmethod
    def get_elevators():
        print("Retrievinig elevators")

    def get_elevator(self, set_as_default=False):
        elevator_from_db = elevator.get_elevator_by_id(self.current_elevator_id)
        if set_as_default:
            self.current_elevator_id = elevator_from_db.get('id')
            self.top_floor = elevator_from_db.get('top_floor')
            self.lower_floor = elevator_from_db.get('lower_floor')
            self.last_record_id = elevator_from_db.get('last_record_id')
            self.is_up = elevator_from_db.get('is_up')
            self.is_vacant = elevator_from_db.get('is_vacant')
            self.is_on_demand = elevator_from_db.get('is_on_demand')
        return elevator_from_db

    def perform_movement(self, current_floor, target_floor, direction, is_vacant, demand_timestamp=datetime.now()):
        arrival_seconds = self.calculate_arrival_time(current_floor, target_floor)
        arrival_timestamp = demand_timestamp + timedelta(seconds=arrival_seconds)

        record_id = elevator.create_elevator_record(self.current_elevator_id,
                                                    current_floor=current_floor,
                                                    target_floor=target_floor,
                                                    direction=direction,
                                                    demand_time=demand_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                    arrival_time=arrival_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                                    is_vacant=is_vacant)
        return record_id

    def save_resting_floor_record(self, resting_floor, resting_floor_arrival_time):

        elevator.create_elevator_record(self.current_elevator_id,
                                        current_floor=resting_floor,
                                        target_floor=resting_floor,
                                        direction=RESTING_DIRECTION,
                                        demand_time=resting_floor_arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
                                        arrival_time=resting_floor_arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
                                        is_vacant=RESTING_FLOOR_IS_VACANT_VALUE)

    def perform_call_movement(self, call_floor, direction):
        if self.is_on_demand:
            last_record = elevator.get_record_by_id(self.last_record_id)
            last_record_demand_timestamp = last_record.get('demand_time')
            last_record_arrival_timestamp = last_record.get('arrival_time')
            last_record_current_floor = last_record.get('current_floor')
            last_record_target_floor = last_record.get('target_floor')

            demand_timestamp = datetime.now()

            if not (last_record_demand_timestamp < demand_timestamp < last_record_arrival_timestamp):

                self.save_resting_floor_record(last_record_target_floor, last_record_arrival_timestamp)

                record_id = self.perform_movement(last_record_target_floor, call_floor, direction, self.is_vacant,
                                                  demand_timestamp=demand_timestamp)
                self.last_record_id = record_id
                elevator.update_elevator(
                    self.current_elevator_id,
                    last_record_id=record_id)

                return record_id

            if not ((self.is_up and direction == 1) or (not self.is_up and direction == -1)):
                record_id = self.perform_movement(last_record_target_floor, call_floor, direction, self.is_vacant,
                                                  demand_timestamp=last_record_arrival_timestamp)
                self.last_record_id = record_id
                elevator.update_elevator(
                    self.current_elevator_id,
                    last_record_id=record_id)

                return record_id

            if not (last_record_current_floor < call_floor < last_record_target_floor):

                record_id = self.perform_movement(last_record_target_floor, call_floor, direction,
                                                  self.is_vacant, demand_timestamp=last_record_arrival_timestamp)
                self.last_record_id = record_id
                elevator.update_elevator(
                    self.current_elevator_id,
                    last_record_id=record_id)

                return record_id

            arrival_seconds = self.calculate_arrival_time(last_record_current_floor, call_floor)
            arrival_timestamp = last_record_demand_timestamp + timedelta(seconds=arrival_seconds)

            if not (demand_timestamp < arrival_timestamp):
                record_id = self.perform_movement(last_record_target_floor, call_floor, direction,
                                                  self.is_vacant, demand_timestamp=last_record_arrival_timestamp)
                self.last_record_id = record_id
                elevator.update_elevator(
                    self.current_elevator_id,
                    last_record_id=record_id)

                return record_id

            record_id = self.perform_movement(last_record_current_floor, call_floor, direction,
                                              self.is_vacant, demand_timestamp=last_record_demand_timestamp)
            return record_id
        else:
            self.is_on_demand = True
            self.is_vacant = True
            record_id = self.perform_movement(self.elevator_floor, call_floor, direction, self.is_vacant)

            if direction < 1:
                self.is_up = False
            else:
                self.is_up = True

            elevator.update_elevator(
                self.current_elevator_id,
                last_record_id=self.last_record_id,
                is_vacant=self.is_vacant,
                is_up=self.is_up)

            self.last_record_id = record_id

            return record_id
        # Update last movement in database if is necessary "YES IT'S COMPLETE NECESSARY"

    def perform_elevator_movement(self, target_floor, is_last_movement=False):
        # On demand movement | normal_movement | and rest record/movement
        last_record = elevator.get_record_by_id(self.last_record_id)
        demand_timestamp = last_record.get('arrival_time')
        current_floor = last_record.get('target_floor')
        direction = last_record.get('direction')

        if self.is_up:
            if target_floor < current_floor:
                return
        else:
            if target_floor > current_floor:
                return

        self.is_vacant = False

        arrival_seconds = self.calculate_arrival_time(current_floor, target_floor)
        arrival_timestamp = demand_timestamp + timedelta(seconds=arrival_seconds)

        record_id = self.perform_movement(current_floor, target_floor, direction, self.is_vacant,
                                          demand_timestamp=demand_timestamp)

        elevator_last_trip = elevator.get_elevator_record_with_higher_timestamp_by_elevator_id(self.current_elevator_id)

        if (elevator_last_trip.get("arrival_time") and
                elevator_last_trip.get("arrival_time") > arrival_timestamp):
            record_id = elevator_last_trip.get("elevator_id")

        elevator.update_elevator(
            self.current_elevator_id,
            is_vacant=self.is_vacant,
            is_up=self.is_up,
            last_record_id=record_id)

        self.last_record_id = record_id
        return record_id
        # Try to use is_las_movement

    @staticmethod
    def calculate_arrival_time(current_floor, target_floor):
        if current_floor * target_floor < 0:
            return abs(current_floor - target_floor) - 1
        else:
            return abs(current_floor - target_floor)


current_elevator = Elevator()
