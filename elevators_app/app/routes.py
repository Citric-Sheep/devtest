from flask import Blueprint, request, jsonify
from app.models import Demand, Elevator
from datetime import datetime
from app.database import db

endpoints = Blueprint('main', __name__)

@endpoints.route('/call_elevator', method=['POST'])
def call_elevator():
    data = request.get_json()
    new_demand = Demand(
        floor = data.get('floor'),
        timestamp = datetime.fromisoformat(data['timestamp']), # TODO Update later to datetime.now
        elevator_id = data.get('elevator_id')
    )
    db.session.add(new_demand)
    db.session.commit()

    return jsonify(""), 201


@endpoints.route('/elevator', methods=['GET', 'POST'])
def update_elevator():
    data = request.get_json()
    elevator = Elevator.query.get(data['elevator_id'])
    if not elevator:
        return jsonify("NOT FOUND ERROR"), 404
    elevator.current_floor = data['current_floor']
    elevator.status = data['status']
    if data['status'] == 'resting':
        resting_history = elevator.current_floor # TODO create a better model
        db.session.add(resting_history)
    db.session.commit()
    return jsonify({'elevator_id': elevator.elevator_id, 'message': 'Elevator updated'}), 200
