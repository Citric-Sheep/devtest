import datetime
from flask import Blueprint, request, jsonify
from database import db
from models import Demand, ElevatorMovement
from process import preprocessing

demand_blueprint = Blueprint("demand", __name__)
elevator_blueprint = Blueprint("elevator", __name__)
predictor_blueprint = Blueprint("predictor", __name__)

# DEMAND ROUTES
@demand_blueprint.route("/demand", methods=["POST"])
def create_demand():
    """Create a new demand."""
    data = request.json
    floor = data.get("floor")

    new_demand = Demand(floor=floor)
    db.session.add(new_demand)
    db.session.commit()

    return jsonify({"message": "Demand created successfully"}), 201

@demand_blueprint.route("/demands", methods=["GET"])
def get_all_demands():
    """Get all demands."""
    demands = Demand.query.all()
    serialized_demands = [demand.serialize() for demand in demands]
    return jsonify(serialized_demands), 200

@demand_blueprint.route("/demand/<int:demand_id>", methods=["GET"])
def get_demand(demand_id):
    """Get a demand by its ID."""
    demand = db.session.get(Demand, demand_id)
    if demand:
        return jsonify(demand.serialize()), 200
    else:
        return jsonify({"message": "Demand not found"}), 404

@demand_blueprint.route("/demand/<int:demand_id>", methods=["PUT"])
def update_demand(demand_id):
    """Update a demand by its ID."""
    data = request.json
    demand = db.session.get(Demand, demand_id)
    if demand:
        # Update demand attributes
        demand.floor = data.get("floor", demand.floor)
        db.session.commit()
        return jsonify({"message": "Demand updated successfully"}), 200
    else:
        return jsonify({"message": "Demand not found"}), 404

@demand_blueprint.route("/demand/<int:demand_id>", methods=["DELETE"])
def delete_demand(demand_id):
    """Delete a demand by its ID."""
    demand = db.session.get(Demand, demand_id)
    if demand:
        db.session.delete(demand)
        db.session.commit()
        return jsonify({"message": "Demand deleted successfully"}), 200
    else:
        return jsonify({"message": "Demand not found"}), 404

# ELEVATOR MOVEMENT ROUTES
@elevator_blueprint.route("/elevator_movement", methods=["POST"])
def create_elevator_movement():
    """Create a new elevator movement."""
    data = request.json
    # Create new ElevatorMovement instance
    timestamp = datetime.datetime.now()
    elevator_id = data.get("elevator_id")
    current_floor = data.get("current_floor")
    next_floor = data.get("next_floor")
    action = data.get("action")
    floor_requested = data.get("floor_requested")
    expected_arrival_time = data.get("expected_arrival_time")
    
    new_movement = ElevatorMovement(timestamp=timestamp, elevator_id=elevator_id, current_floor=current_floor, next_floor=next_floor, action=action, floor_requested=floor_requested, expected_arrival_time=expected_arrival_time)
    db.session.add(new_movement)
    db.session.commit()

    return jsonify({"message": "Elevator movement created successfully"}), 201

@elevator_blueprint.route("/elevator_movements", methods=["GET"])
def get_all_elevator_movements():
    """Get all elevator movements."""
    movements = ElevatorMovement.query.all()
    serialized_movements = [movement.serialize() for movement in movements]
    return jsonify(serialized_movements), 200

@elevator_blueprint.route("/elevator_movement/<int:elevator_movement_id>", methods=["GET"])
def get_elevator_movement(elevator_movement_id):
    """Get an elevator movement by its ID."""
    movement = db.session.get(ElevatorMovement, elevator_movement_id)
    if movement:
        return jsonify(movement.serialize()), 200
    else:
        return jsonify({"message": "Elevator movement not found"}), 404

@elevator_blueprint.route("/elevator_movement/<int:elevator_movement_id>", methods=["PUT"])
def update_elevator_movement(elevator_movement_id):
    """Update an elevator movement by its ID."""
    data = request.json
    movement = db.session.get(ElevatorMovement, elevator_movement_id)
    if movement:
        # Update movement attributes
        movement.elevator_id = data.get("elevator_id", movement.elevator_id)
        movement.current_floor = data.get("current_floor", movement.current_floor)
        movement.next_floor = data.get("next_floor", movement.next_floor)
        movement.action = data.get("action", movement.action)
        movement.floor_requested = data.get("floor_requested", movement.floor_requested)
        movement.expected_arrival_time = data.get("expected_arrival_time", movement.expected_arrival_time)
        
        db.session.commit()
        return jsonify({"message": "Elevator movement updated successfully"}), 200
    else:
        return jsonify({"message": "Elevator movement not found"}), 404

@elevator_blueprint.route("/elevator_movement/<int:elevator_movement_id>", methods=["DELETE"])
def delete_elevator_movement(elevator_movement_id):
    """Delete an elevator movement by its ID."""
    movement = db.session.get(ElevatorMovement, elevator_movement_id)
    if movement:
        db.session.delete(movement)
        db.session.commit()
        return jsonify({"message": "Elevator movement deleted successfully"}), 200
    else:
        return jsonify({"message": "Elevator movement not found"}), 404

# PREDICTOR
@predictor_blueprint.route("/predictor/preprocessing", methods=["GET"])
def preprocessing_route():
    """
    Endpoint for preprocessing data.
    
    This method preprocesses data based on the provided 'min_stops' parameter,
    then returns the processed data in JSON format.
    """
    min_stops = request.args.get("min_stops", 1)  # Get the value of 'min_stops' from the query string or set the default value to 1 if not provided
    floor_data = preprocessing(min_stops)  # Call the preprocessing function to perform data processing
    return jsonify([vars(item) for item in floor_data])  # Convert 'FloorData' objects into dictionaries and return them as JSON

