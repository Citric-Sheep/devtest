class Floor:
    def __init__(self, floor_number: int = 0) -> None:
        """
        Initialize a new Floor object.

        Args:
            floor_number (int): The floor number.

        Returns:
            None
        """
        self.floor_number = floor_number

    def get_floor_number(self) -> int:
        """
        Get the floor number.

        Returns:
            int: The floor number.
        """
        return self.floor_number
    
    def set_floor_number(self, floor_number) -> None:
        """
        Set the floor number.

        Args:
            floor_number (int): The new floor number.

        Returns:
            None
        """
        self.floor_number = floor_number

    def __str__(self) -> str:
        """
        Get a string representation of the Floor object.

        Returns:
            str: A string representation of the Floor object.
        """
        return "Floor " + str(self.floor_number)