from datetime import datetime
from .enums import Status
from .mongo import create_log


MAX_FLOOR = 10
MIN_FLOOR = -1
MAX_WEIGHT = 900.0 # kilograms

class Elevator:
    def __init__(self) -> None:
        self.current_floor = 0
        self.weight = 0.0

    def is_floor_valid(self, floor : int) -> bool:
        if floor < MIN_FLOOR:
            return False
        if floor > MAX_FLOOR:
            return False
        return True
    
    def process_demand(self, 
              src_floor : int, 
              dest_floor : int,
              load_weight : float
              ) -> dict:
        '''
        Guard Cases
        '''
        if not self.is_floor_valid(src_floor) or not self.is_floor_valid(dest_floor):
            return {"error" : "Invalid Floor"}
        
        if src_floor == dest_floor:
            return {"error" : "Source Floor equals Destination Floor"}

        if load_weight > MAX_WEIGHT:
            return {"error" : "Overweight load"}
        rest_floor = self.current_floor
        
        
        if not self.current_floor == src_floor:
            _ = self.process_demand(self.current_floor, src_floor, load_weight=0)
        
        # Operating
        log = {
            'status' : Status.RUNNING.value,
            'src_floor' : src_floor,
            'dest_floor' : dest_floor,
            'rest_floor' : rest_floor,
            'start_timestamp' : datetime.now(),
            'weight' : load_weight
        }
        create_log(log)

        # Done
        self.current_floor = dest_floor

        finish_log = {
            'status' : Status.IDDLE.value,
            'rest_floor' : self.current_floor,
            'timestamp' : datetime.now()
        }
        create_log(finish_log)
        
        return {"message" : "OK"}

