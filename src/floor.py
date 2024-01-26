class Floor:
    def __init__(self, floor_number: int = 0) -> None:
        self.floor_number = floor_number

    def get_floor_number(self) -> int:
        return self.floor_number
    
    def set_floor_number(self, floor_number) -> None:
        self.floor_number = floor_number

    def __str__(self) -> str:
        return "Floor " + str(self.floor_number)