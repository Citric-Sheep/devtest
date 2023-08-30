##############
# Libraries #
##############

from typing import List
from enum import Enum


###################
# Elevator logic #
###################

class Direction(Enum):
    STATIONARY = 3
    DOWN = 2
    UP = 1


class Elevator:
    def __init__(self,
                 request_queue: List,
                 direction: int = 3,
                 current_floor: int = 1):
        self.current_floor = current_floor
        self.direction = Direction(direction)
        self.request_queue = request_queue

    def target_floor(self):
        if self.direction == self.direction.STATIONARY:
            sorted_queue = sorted(self.request_queue, key=lambda x: x.elevator_order_created_on)
            if sorted_queue:
                target_floor = sorted_queue[0].elevator_order_demand_floor
                request_id = sorted_queue[0].elevator_order_id
            else:
                target_floor = self.current_floor
                request_id = None
        elif self.direction == self.direction.DOWN:
            down_queue = []
            up_queue = []
            for record in self.request_queue:
                floor_and_id = (record.elevator_order_demand_floor, record.elevator_order_id)
                if record.elevator_order_demand_category == 1:
                    if record.elevator_order_demand_type == 2:
                        if record.elevator_order_demand_floor < self.current_floor:
                            down_queue.append(floor_and_id)
                        else:
                            up_queue.append(floor_and_id)
                    elif record.elevator_order_demand_type == 1:
                        up_queue.append(floor_and_id)
                if record.elevator_order_demand_category == 2:
                    if record.elevator_order_demand_floor < self.current_floor:
                        down_queue.append(floor_and_id)
            if down_queue:
                target_floor, request_id = max(down_queue, key=lambda x: x[0])
            elif up_queue:
                target_floor, request_id = min(up_queue, key=lambda x: x[0])
            else:
                target_floor = self.current_floor
                request_id = None
        elif self.direction == self.direction.UP:
            down_queue = []
            up_queue = []
            for record in self.request_queue:
                floor_and_id = (record.elevator_order_demand_floor, record.elevator_order_id)
                if record.elevator_order_demand_category == 1:
                    if record.elevator_order_demand_type == 1:
                        if record.elevator_order_demand_floor > self.current_floor:
                            up_queue.append(floor_and_id)
                        else:
                            down_queue.append(floor_and_id)
                    elif record.elevator_order_demand_type == 2:
                        down_queue.append(floor_and_id)
                if record.elevator_order_demand_category == 2:
                    if record.elevator_order_demand_floor > self.current_floor:
                        up_queue.append(floor_and_id)
            if up_queue:
                target_floor, request_id = min(up_queue, key=lambda x: x[0])
            elif down_queue:
                target_floor, request_id = max(down_queue, key=lambda x: x[0])
            else:
                target_floor = self.current_floor
                request_id = None
        else:
            target_floor = self.current_floor
            request_id = None
        return {'target_floor': target_floor, 'request_id': request_id}
