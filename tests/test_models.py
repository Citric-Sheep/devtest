from datetime import datetime, timedelta
import pytest
from src.models import Building, Elevator, ElevatorCall, ElevatorTrip, ElevatorState, TimeStatistic, FloorStatistic

class TestBuilding:
    def test_create_building(self, db_session):
        building = Building(name="Test Building", floors=10)
        db_session.add(building)
        db_session.commit()
        
        assert building.id is not None
        assert building.name == "Test Building"
        assert building.floors == 10
        assert building.created_at is not None
    
    def test_building_elevator_relationship(self, db_session, sample_building):
        elevator = Elevator(building_id=sample_building.id, name="Test Elevator")
        db_session.add(elevator)
        db_session.commit()
        
        db_session.refresh(sample_building)
        assert len(sample_building.elevators) == 1
        assert sample_building.elevators[0].name == "Test Elevator"

class TestElevator:
    def test_create_elevator(self, db_session, sample_building):
        elevator = Elevator(building_id=sample_building.id, name="Test Elevator")
        db_session.add(elevator)
        db_session.commit()
        
        assert elevator.id is not None
        assert elevator.name == "Test Elevator"
        assert elevator.building_id == sample_building.id
        assert elevator.created_at is not None
    
    def test_elevator_building_relationship(self, db_session, sample_elevator):
        assert sample_elevator.building is not None
        assert sample_elevator.building.name == "Test Building"
    
    def test_current_state(self, db_session, sample_elevator):
        # No state yet
        assert sample_elevator.current_state(db_session) is None
        
        # Add a state
        state = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=5,
            is_vacant=True,
            is_moving=False
        )
        db_session.add(state)
        db_session.commit()
        
        current_state = sample_elevator.current_state(db_session)
        assert current_state is not None
        assert current_state.floor == 5
        assert current_state.is_vacant is True
        assert current_state.is_moving is False
    
    def test_is_resting(self, db_session, sample_elevator):
        # No state yet
        assert sample_elevator.is_resting(db_session) is False
        
        # Add a non-resting state (moving)
        state1 = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=5,
            is_vacant=True,
            is_moving=True
        )
        db_session.add(state1)
        db_session.commit()
        
        assert sample_elevator.is_resting(db_session) is False
        
        # Add a resting state
        state2 = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=7,
            is_vacant=True,
            is_moving=False
        )
        db_session.add(state2)
        db_session.commit()
        
        assert sample_elevator.is_resting(db_session) is True
        
        # Add a non-resting state (occupied)
        state3 = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=3,
            is_vacant=False,
            is_moving=False
        )
        db_session.add(state3)
        db_session.commit()
        
        assert sample_elevator.is_resting(db_session) is False
    
    def test_resting_floor(self, db_session, sample_elevator):
        # No state yet
        assert sample_elevator.resting_floor(db_session) is None
        
        # Add a non-resting state
        state1 = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=5,
            is_vacant=True,
            is_moving=True
        )
        db_session.add(state1)
        db_session.commit()
        
        assert sample_elevator.resting_floor(db_session) is None
        
        # Add a resting state
        state2 = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=7,
            is_vacant=True,
            is_moving=False
        )
        db_session.add(state2)
        db_session.commit()
        
        assert sample_elevator.resting_floor(db_session) == 7

class TestElevatorCall:
    def test_create_call(self, db_session, sample_elevator):
        call = ElevatorCall(
            elevator_id=sample_elevator.id,
            floor=3,
            direction="up"
        )
        db_session.add(call)
        db_session.commit()
        
        assert call.id is not None
        assert call.elevator_id == sample_elevator.id
        assert call.floor == 3
        assert call.direction == "up"
        assert call.timestamp is not None
        assert call.wait_time is None
    
    def test_elevator_call_relationship(self, db_session, sample_elevator):
        call = ElevatorCall(
            elevator_id=sample_elevator.id,
            floor=3,
            direction="up"
        )
        db_session.add(call)
        db_session.commit()
        
        db_session.refresh(sample_elevator)
        assert len(sample_elevator.calls) == 1
        assert sample_elevator.calls[0].floor == 3

class TestElevatorTrip:
    def test_create_trip(self, db_session, sample_elevator):
        start_time = datetime.now()
        trip = ElevatorTrip(
            elevator_id=sample_elevator.id,
            start_time=start_time,
            origin_floor=2,
            destination_floor=8,
            occupancy=True
        )
        db_session.add(trip)
        db_session.commit()
        
        assert trip.id is not None
        assert trip.elevator_id == sample_elevator.id
        assert trip.start_time == start_time
        assert trip.end_time is None
        assert trip.origin_floor == 2
        assert trip.destination_floor == 8
        assert trip.occupancy is True
    
    def test_trip_duration(self, db_session, sample_elevator):
        start_time = datetime.now()
        trip = ElevatorTrip(
            elevator_id=sample_elevator.id,
            start_time=start_time,
            origin_floor=2,
            destination_floor=8,
            occupancy=True
        )
        db_session.add(trip)
        db_session.commit()
        
        # No end time yet
        assert trip.duration() is None
        
        # Add end time
        end_time = start_time + timedelta(seconds=30)
        trip.end_time = end_time
        db_session.commit()
        
        assert trip.duration() == 30.0

class TestElevatorState:
    def test_create_state(self, db_session, sample_elevator):
        state = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=5,
            is_vacant=True,
            is_moving=False
        )
        db_session.add(state)
        db_session.commit()
        
        assert state.id is not None
        assert state.elevator_id == sample_elevator.id
        assert state.floor == 5
        assert state.is_vacant is True
        assert state.is_moving is False
        assert state.timestamp is not None
    
    def test_is_resting_property(self, db_session, sample_elevator):
        # Resting state
        state1 = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=5,
            is_vacant=True,
            is_moving=False
        )
        assert state1.is_resting is True
        
        # Not resting - moving
        state2 = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=5,
            is_vacant=True,
            is_moving=True
        )
        assert state2.is_resting is False
        
        # Not resting - occupied
        state3 = ElevatorState(
            elevator_id=sample_elevator.id,
            floor=5,
            is_vacant=False,
            is_moving=False
        )
        assert state3.is_resting is False

class TestStatistics:
    def test_create_time_statistic(self, db_session, sample_elevator):
        stat = TimeStatistic(
            elevator_id=sample_elevator.id,
            date=datetime.now().date(),
            hour=14,
            calls_count=5,
            most_common_origin_floor=3,
            most_common_destination_floor=7
        )
        db_session.add(stat)
        db_session.commit()
        
        assert stat.id is not None
        assert stat.elevator_id == sample_elevator.id
        assert stat.hour == 14
        assert stat.calls_count == 5
        assert stat.most_common_origin_floor == 3
        assert stat.most_common_destination_floor == 7
    
    def test_create_floor_statistic(self, db_session, sample_elevator):
        stat = FloorStatistic(
            elevator_id=sample_elevator.id,
            floor=3,
            date=datetime.now().date(),
            calls_count=7,
            avg_wait_time=15.5
        )
        db_session.add(stat)
        db_session.commit()
        
        assert stat.id is not None
        assert stat.elevator_id == sample_elevator.id
        assert stat.floor == 3
        assert stat.calls_count == 7
        assert stat.avg_wait_time == 15.5