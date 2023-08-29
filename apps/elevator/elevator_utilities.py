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
        elif self.direction == 2:
            down_queue = []
            up_queue = []
            for record in self.request_queue:
                if record.elevator_order_demand_category == 1:
                    if record.elevator_order_demand_type == 2:
                        if record.elevator_order_demand_floor < self.current_floor:
                            down_queue.append(record.elevator_order_demand_floor)
                        else:
                            up_queue.append(record.elevator_order_demand_floor)
                    elif record.elevator_order_demand_type == 1:
                        up_queue.append(record.elevator_order_demand_floor)
                if record.elevator_order_demand_category == 2:
                    if record.elevator_order_demand_floor < self.current_floor:
                        down_queue.append(record.elevator_order_demand_floor)
            if down_queue:
                target_floor = max(down_queue)
            elif up_queue:
                target_floor = min(up_queue)
            else:
                target_floor = self.current_floor
        elif self.direction == 1:
            down_queue = []
            up_queue = []
            for record in self.request_queue:
                if record.elevator_order_demand_category == 1:
                    if record.elevator_order_demand_type == 1:
                        if record.elevator_order_demand_floor > self.current_floor:
                            up_queue.append(record.elevator_order_demand_floor)
                        else:
                            down_queue.append(record.elevator_order_demand_floor)
                    elif record.elevator_order_demand_type == 2:
                        down_queue.append(record.elevator_order_demand_floor)
                if record.elevator_order_demand_category == 2:
                    if record.elevator_order_demand_floor > self.current_floor:
                        up_queue.append(record.elevator_order_demand_floor)
            if up_queue:
                target_floor = min(up_queue)
            elif down_queue:
                target_floor = max(down_queue)
            else:
                target_floor = self.current_floor
        else:
            target_floor = self.current_floor
        return {'target_floor': target_floor}
