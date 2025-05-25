# -*- coding: utf-8 -*-
from typing import Dict,Any,Optional
from datetime import datetime
from app import db
from app.models import ElevatorDemand,ElevatorState
from app.validations import validate_floor, validate_state

def create_demand(data:Dict[str,int]) -> None:
    '''
    Create a new instance of ElevatorDemand. Raise ValueError if the validation fails

    Parameters
    ----------
    data : Dict[str,int]
        contains the actual and target floor.

    Raises
    ------
    ValueError
        If the floor validation fails.

    Returns
    -------
    None

    '''
    actual_floor = data.get("actual_floor")
    target_floor = data.get("target_floor")
    if not validate_floor(actual_floor) or not validate_floor(target_floor):
        raise ValueError("Floor is not an integer")
    new_demand = ElevatorDemand(actual_floor=actual_floor,target_floor=target_floor)
    db.session.add(new_demand)
    db.session.commit()
    return


def create_state(data:Dict[str,Any]) -> None:
    '''
    Create a new instance of ElevatorState. Raise ValueError if the vacant or floor 
    validation fails 

    Parameters
    ----------
    data : Dict[str,Any]
        Contains the actual floor of the elevator and if it is vacant. 

    Raises
    ------
    ValueError
        If the floor or state validation fails

    Returns
    -------
    None

    '''
    floor = data.get("floor")
    vacant = data.get("vacant")
    if not validate_floor(floor):
        raise ValueError("Floor is not an integer")
    if not validate_state(vacant):
        raise ValueError("Vacant invalid")
    new_state = ElevatorState(floor=floor, vacant=vacant)
    db.session.add(new_state)
    db.session.commit()
    return
    
def change_state(state_id:int, data:Dict[str,str]) -> Optional[ElevatorState]:
    '''
    Triggers the change of state adding end_time and duration to a ElevatorState instance

    Parameters
    ----------
    state_id : int
        ID of the state.
    data : Dict[str,str]
        Contains the end_time in isoformat.

    Returns
    -------
    Optional[ElevatorState]
        Returns an instance of ElevatorState if exist for state_id else None.

    '''
    end_time = data.get("end_time")
    end_time = datetime.fromisoformat(end_time)
    state = ElevatorState.query.filter_by(id=state_id).first()
    if not state:
        return state
    state.end_time = end_time
    state.duration_sec = int((end_time - state.start_time).total_seconds())
    
    #Business Rule: Idle Relocation
    state.relocation_flag = state.duration_sec > 300
    db.session.commit()
    return state    

    
        
        
        
        
        
    