# -*- coding: utf-8 -*-


def validate_floor(floor:int) -> bool:
    '''
    Validate if the floor is an integer. More restrictions could be implemented 
    in particular cases (e.g. top and bottom floor)

    Parameters
    ----------
    floor : int
        The floor number.

    Returns
    -------
    bool
        True if the floor is an integer.

    '''
    if isinstance(floor, int):
        return True
    return False

def validate_state(vacant:bool) -> bool:
    '''
    Validate if the elevator is vacant

    Parameters
    ----------
    vacant : bool
        True if the elevator is vacant.

    Returns
    -------
    bool
        True if vacant is a bool, else False.

    '''
    if isinstance(vacant, bool):
        return True
    return False

