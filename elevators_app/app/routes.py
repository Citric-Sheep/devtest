from flask import Blueprint, request, jsonify
from app.models import Demand, Elevator, ElevatorHistory
from datetime import datetime
from app.database import db

endpoints = Blueprint('main', __name__)

@endpoints.route('/call_elevator', methods=['POST'])
def call_elevator():
    data = request.get_json()
    new_demand = Demand(
        floor_number = data.get('floor'),
        timestamp = datetime.fromisoformat(data['timestamp']), # TODO Update later to datetime.now
        elevator_id = data.get('elevator_id')
    )
    db.session.add(new_demand)
    db.session.commit()

    return jsonify(""), 201


@endpoints.route('/elevator', methods=['POST'])
def update_elevator():
    data = request.get_json()
    elevator = Elevator.query.get(data['elevator_id'])
    if not elevator:
        return jsonify("NOT FOUND ERROR"), 404
    elevator.current_floor = data['current_floor']
    elevator.status = data['status']
    if data['status'] == 'resting':
        resting_history = ElevatorHistory(
            elevator_id = elevator.elevator_id,
            resting_floor = elevator.current_floor,
            timestamp=datetime.utcnow()
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


@endpoints.route('/elevator/teste', methods=['GET'])
def get_teste():
    new_demand = Demand(
        floor_number = 999,
        timestamp = datetime.now,
        elevator_id = 1
    )
    db.session.add(new_demand)
    db.session.commit()
    return jsonify({"msg":"TESTE"}), 200