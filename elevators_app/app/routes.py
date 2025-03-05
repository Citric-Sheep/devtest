from flask import Blueprint, request, jsonify
from app.models import Demand, Elevator, ElevatorHistory
from datetime import datetime
from app.database import db

endpoints = Blueprint('main', __name__)

@endpoints.route('/elevator', methods=['POST'])
def create_elevador():
    new_elevator = Elevator(
        current_floor=0,
        status="idle",
        resting_floor=0
    )
    db.session.add(new_elevator)
    db.session.commit()

    return jsonify({
        "elevator_id": new_elevator.elevator_id,
        "message": "Elevator created successfully"
    }), 201

@endpoints.route('/call_elevator', methods=['POST'])
def call_elevator():
    data = request.get_json()
    #TODO add error handling
    new_demand = Demand(
        floor_number = data.get('floor'),
        elevator_id = data.get('elevator_id')
    )
    db.session.add(new_demand)
    db.session.commit()

    return jsonify({"message": "Elevator on the way"}), 201


@endpoints.route('/elevator/update', methods=['POST'])
def update_elevator():
    data = request.get_json()
    elevator = Elevator.query.get(data['elevator_id'])
    if not elevator:
        return jsonify("NOT FOUND ERROR"), 404
    elevator.current_floor = data['current_floor']
    elevator.status = data.get("status")
    if elevator.status == "idle":
        resting_history = ElevatorHistory(
                elevator_id = elevator.elevator_id,
                resting_floor = elevator.current_floor,
            ) 
        db.session.add(resting_history)
        db.session.commit()
    return jsonify({'elevator_id': elevator.elevator_id, 'message': 'Elevator updated'}), 200

@endpoints.route('/elevator/history', methods=['GET'])
def get_elevator_history():
    elevator_id = request.args.get('elevator_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    query = ElevatorHistory.query.filter_by(elevator_id=elevator_id)
    if start_time:
        query = query.filter(ElevatorHistory.timestamp >= start_time)
    if end_time:
        query = query.filter(ElevatorHistory.timestamp <= end_time)

    resting_floors = query.all()
    return jsonify([{
        'resting_floor': floor.resting_floor,
        'timestamp': floor.timestamp.isoformat()
    } for floor in resting_floors]), 200