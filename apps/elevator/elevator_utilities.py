###################
# Elevator logic #
###################

class Elevator:
    def __init__(self, request_queue, direction=3, current_floor=1):
        self.current_floor = current_floor
        self.direction = direction
        self.request_queue = request_queue

    def target_floor(self):
        if self.direction == 3:
            sorted_queue = sorted(self.request_queue, key=lambda x: x.elevator_order_update_on)
            target_floor = sorted_queue[0].elevator_order_demand_floor
            request_id = sorted_queue[0].elevator_order_id
        elif self.direction == 2:
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
        elif self.direction == 1:
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
