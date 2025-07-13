import os
from datetime import datetime, date
from flask import Flask, request, jsonify, abort
from sqlalchemy import func

from src.db import init_db, get_db_session
from src.models import *

app = Flask(__name__)

# Init DB
@app.before_first_request
def setup():
    init_db()

# Error stuff
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request", "msg": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "msg": str(error)}), 404

# Buildings
@app.route('/buildings', methods=['GET'])
def get_buildings():
    with get_db_session() as s:
        buildings = s.query(Building).all()
        return jsonify([{
            'id': b.id,
            'name': b.name,
            'floors': b.floors,
            'created_at': b.created_at.isoformat()
        } for b in buildings])

@app.route('/buildings', methods=['POST'])
def create_building():
    data = request.get_json()
    
    # Check required fields
    if not data or 'name' not in data or 'floors' not in data:
        abort(400, "Missing required fields")
    
    with get_db_session() as s:
        b = Building(name=data['name'], floors=data['floors'])
        s.add(b)
        s.commit()
        
        return jsonify({
            'id': b.id,
            'name': b.name,
            'floors': b.floors,
            'created_at': b.created_at.isoformat()
        }), 201

# Elevators
@app.route('/buildings/<int:building_id>/elevators', methods=['POST'])
def create_elevator(building_id):
    data = request.get_json()
    
    if not data or 'name' not in data:
        abort(400, "Need elevator name")
    
    with get_db_session() as s:
        # Find building
        building = s.query(Building).filter(Building.id == building_id).first()
        
        if not building:
            abort(404, f"No building #{building_id}")
        
        # Create elevator
        elev = Elevator(building_id=building_id, name=data['name'])
        s.add(elev)
        s.commit()
        
        return jsonify({
            'id': elev.id,
            'name': elev.name,
            'building_id': elev.building_id,
            'created_at': elev.created_at.isoformat()
        }), 201

# Elevator calls
@app.route('/elevators/<int:elevator_id>/calls', methods=['POST'])
def create_elevator_call(elevator_id):
    # Record elevator call and update stats
    data = request.get_json()
    
    if not data or 'floor' not in data or 'direction' not in data:
        abort(400, "Need floor and direction")
    
    if data['direction'] not in ['up', 'down']:
        abort(400, "Direction must be up/down")
    
    with get_db_session() as s:
        # Find elevator
        elev = s.query(Elevator).filter(Elevator.id == elevator_id).first()
        if not elev:
            abort(404, f"No elevator #{elevator_id}")
        
        # Check floor
        building = s.query(Building).filter(Building.id == elev.building_id).first()
        if data['floor'] < 1 or data['floor'] > building.floors:
            abort(400, f"Invalid floor number")
        
        # Make the call
        call = ElevatorCall(
            elevator_id=elevator_id,
            floor=data['floor'],
            direction=data['direction']
        )
        s.add(call)
        
        # Update stats
        today = date.today()
        hour = datetime.now().hour
        
        # Time stats
        time_stat = s.query(TimeStatistic).filter(
            TimeStatistic.elevator_id == elevator_id,
            TimeStatistic.date == today,
            TimeStatistic.hour == hour
        ).first()
        
        if time_stat:
            time_stat.calls_count += 1
        else:
            time_stat = TimeStatistic(
                elevator_id=elevator_id,
                date=today,
                hour=hour,
                calls_count=1
            )
            s.add(time_stat)
        
        # Floor stats
        floor_stat = s.query(FloorStatistic).filter(
            FloorStatistic.elevator_id == elevator_id,
            FloorStatistic.floor == data['floor'],
            FloorStatistic.date == today
        ).first()
        
        if floor_stat:
            floor_stat.calls_count += 1
        else:
            floor_stat = FloorStatistic(
                elevator_id=elevator_id,
                floor=data['floor'],
                date=today,
                calls_count=1
            )
            s.add(floor_stat)
        
        s.commit()
        
        return jsonify({
            'id': call.id,
            'elevator_id': call.elevator_id,
            'timestamp': call.timestamp.isoformat(),
            'floor': call.floor,
            'direction': call.direction
        }), 201

# Elevator states
@app.route('/elevators/<int:elevator_id>/states', methods=['POST'])
def create_elevator_state(elevator_id):
    # Save current elevator state
    data = request.get_json()
    
    # Check data
    if not data or not all(f in data for f in ['floor', 'is_vacant', 'is_moving']):
        abort(400, "Missing required fields")
    
    with get_db_session() as s:
        # Check elevator exists
        elev = s.query(Elevator).filter(Elevator.id == elevator_id).first()
        if not elev:
            abort(404, f"No elevator #{elevator_id}")
        
        # Save state
        state = ElevatorState(
            elevator_id=elevator_id,
            floor=data['floor'],
            is_vacant=data['is_vacant'],
            is_moving=data['is_moving']
        )
        s.add(state)
        s.commit()
        
        # Return state info
        return jsonify({
            'id': state.id,
            'elevator_id': state.elevator_id,
            'timestamp': state.timestamp.isoformat(),
            'floor': state.floor,
            'is_vacant': state.is_vacant,
            'is_moving': state.is_moving,
            'is_resting': state.is_resting
        }), 201

# Trips
@app.route('/elevators/<int:elevator_id>/trips', methods=['POST'])
def create_elevator_trip(elevator_id):
    data = request.get_json()
    
    # Check data
    needed = ['origin_floor', 'destination_floor', 'occupancy']
    if not data or not all(field in data for field in needed):
        abort(400, "Missing trip data")
    
    with get_db_session() as s:
        # Check elevator
        elev = s.query(Elevator).filter(Elevator.id == elevator_id).first()
        if not elev:
            abort(404, f"No elevator #{elevator_id}")
        
        # Create trip
        trip = ElevatorTrip(
            elevator_id=elevator_id,
            start_time=datetime.now(),
            origin_floor=data['origin_floor'],
            destination_floor=data['destination_floor'],
            occupancy=data['occupancy']
        )
        s.add(trip)
        s.commit()
        
        # Return trip info
        return jsonify({
            'id': trip.id,
            'elevator_id': trip.elevator_id,
            'start_time': trip.start_time.isoformat(),
            'origin_floor': trip.origin_floor,
            'destination_floor': trip.destination_floor,
            'occupancy': trip.occupancy
        }), 201

@app.route('/elevators/<int:elevator_id>/trips/<int:trip_id>/complete', methods=['POST'])
def complete_elevator_trip(elevator_id, trip_id):
    # Mark trip as complete and update wait times
    with get_db_session() as s:
        # Find elevator
        elev = s.query(Elevator).filter(Elevator.id == elevator_id).first()
        if not elev:
            abort(404, f"No elevator #{elevator_id}")
        
        # Find trip
        trip = s.query(ElevatorTrip).filter(
            ElevatorTrip.id == trip_id,
            ElevatorTrip.elevator_id == elevator_id
        ).first()
        
        if not trip:
            abort(404, f"Trip not found")
        
        if trip.end_time:
            abort(400, "Already completed")
        
        # End the trip
        trip.end_time = datetime.now()
        
        # Update wait times if empty elevator
        if not trip.occupancy:
            # Find matching call
            call = s.query(ElevatorCall).filter(
                ElevatorCall.elevator_id == elevator_id,
                ElevatorCall.floor == trip.destination_floor,
                ElevatorCall.wait_time.is_(None)
            ).order_by(ElevatorCall.timestamp.desc()).first()
            
            if call:
                # Calculate wait time
                call.wait_time = int((trip.end_time - call.timestamp).total_seconds())
                
                # Update stats
                today = date.today()
                floor_stat = s.query(FloorStatistic).filter(
                    FloorStatistic.elevator_id == elevator_id,
                    FloorStatistic.floor == call.floor,
                    FloorStatistic.date == today
                ).first()
                
                if floor_stat:
                    if floor_stat.avg_wait_time:
                        # Update average
                        prev = floor_stat.avg_wait_time * (floor_stat.calls_count - 1)
                        floor_stat.avg_wait_time = (prev + call.wait_time) / floor_stat.calls_count
                    else:
                        floor_stat.avg_wait_time = call.wait_time
        
        s.commit()
        
        # Return trip data
        return jsonify({
            'id': trip.id,
            'elevator_id': trip.elevator_id,
            'start_time': trip.start_time.isoformat(),
            'end_time': trip.end_time.isoformat(),
            'origin_floor': trip.origin_floor,
            'destination_floor': trip.destination_floor,
            'occupancy': trip.occupancy,
            'duration': trip.trip_time()
        })

# Stats for ML
@app.route('/ml/time_statistics', methods=['GET'])
def get_time_statistics():
    # Get stats by time
    elev_id = request.args.get('elevator_id', type=int)
    date_str = request.args.get('date')
    
    with get_db_session() as s:
        q = s.query(TimeStatistic)
        
        # Apply filters
        if elev_id:
            q = q.filter(TimeStatistic.elevator_id == elev_id)
        
        if date_str:
            try:
                d = datetime.strptime(date_str, '%Y-%m-%d').date()
                q = q.filter(TimeStatistic.date == d)
            except ValueError:
                abort(400, "Bad date format")
        
        # Get results
        stats = q.all()
        
        # Format response
        return jsonify([{
            'elevator_id': stat.elevator_id,
            'date': stat.date.isoformat(),
            'hour': stat.hour,
            'calls_count': stat.calls_count,
            'most_common_origin_floor': stat.most_common_origin_floor,
            'most_common_destination_floor': stat.most_common_destination_floor
        } for stat in stats])

@app.route('/ml/floor_statistics', methods=['GET'])
def get_floor_statistics():
    # Get stats by floor
    elev_id = request.args.get('elevator_id', type=int)
    floor = request.args.get('floor', type=int)
    date_str = request.args.get('date')
    
    with get_db_session() as s:
        q = s.query(FloorStatistic)
        
        # Filters
        if elev_id:
            q = q.filter(FloorStatistic.elevator_id == elev_id)
        
        if floor:
            q = q.filter(FloorStatistic.floor == floor)
        
        if date_str:
            try:
                d = datetime.strptime(date_str, '%Y-%m-%d').date()
                q = q.filter(FloorStatistic.date == d)
            except ValueError:
                abort(400, "Bad date format")
        
        # Get data
        stats = q.all()
        
        # Format response
        return jsonify([{
            'elevator_id': stat.elevator_id,
            'floor': stat.floor,
            'date': stat.date.isoformat(),
            'calls_count': stat.calls_count,
            'avg_wait_time': stat.avg_wait_time
        } for stat in stats])

@app.route('/ml/optimal_resting_floor', methods=['GET'])
def get_optimal_resting_floor():
    # Find best floor for elevator to wait at
    elev_id = request.args.get('elevator_id', type=int)
    
    if not elev_id:
        abort(400, "Need elevator_id")
    
    with get_db_session() as s:
        # Check elevator exists
        elev = s.query(Elevator).filter(Elevator.id == elev_id).first()
        if not elev:
            abort(404, f"No elevator #{elev_id}")
        
        # Get current hour
        hour = datetime.now().hour
        
        # Try to find best floor based on time stats
        time_stat = s.query(TimeStatistic).filter(
            TimeStatistic.elevator_id == elev_id,
            TimeStatistic.hour == hour
        ).order_by(TimeStatistic.date.desc()).first()
        
        if time_stat and time_stat.most_common_origin_floor:
            best_floor = time_stat.most_common_origin_floor
        else:
            # Try floor with most calls today
            today = date.today()
            floor_stat = s.query(FloorStatistic).filter(
                FloorStatistic.elevator_id == elev_id,
                FloorStatistic.date == today
            ).order_by(FloorStatistic.calls_count.desc()).first()
            
            if floor_stat:
                best_floor = floor_stat.floor
            else:
                # Just use ground floor
                best_floor = 1
        
        return jsonify({
            'elevator_id': elev_id,
            'optimal_resting_floor': best_floor,
            'timestamp': datetime.now().isoformat()
        })

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)