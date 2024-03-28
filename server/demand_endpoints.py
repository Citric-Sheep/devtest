from flask import Blueprint, jsonify, request
from controllers.demand_controllers import *

demand_blueprint = Blueprint('demand', __name__)


# Endpoint for retrieving all elevators in a demand
@demand_blueprint.route('/get', defaults={'elevator_id': None}, methods=['GET'])
@demand_blueprint.route('/get/<int:elevator_id>', methods=['GET'])
def get_demands(elevator_id):
    """
    Call this endpoint when you want to retrieve all elevators demands entries in the DB.
    Elevator ID can be passed as query param. If not passed, it will return demands from all elevators.
    """
    return get_demand_controller(elevator_id)


# Endpoint for creating elevators in a demand
@demand_blueprint.route('/create', methods=['POST'])
def create_demand():
    """
    Call this endpoint to create a new demand entry in DB. Elevator should be created previously so that elevator ID is 
    available to create the relationship.
    """
    data = request.json
    keys = ["elevator_id", "start_floor", "end_floor"]
    if not all([key in data for key in keys]):
        return jsonify({'error': 'start_floor, end_floor are required'}), 400
    
    return create_demand_controller(data)


@demand_blueprint.route('/update', methods=['PUT'])
def update_demands():
    keys = ["id", "new_values"]
    data = request.json
    """
    Call this endpoint to update a demand entry in the DB.
    Expected body:

    {
        "id": 2,
        "new_values":
            {
                "end_floor": 3
            }
    }

    So the demand with ID 2 is going to be updated with the end floor 3
    """
    if not all((key in data for key in keys)):
        return jsonify(
            {
                'error': '''demand ID is required for updating it in DB.
                 Please do a GET request to "demand/get" to obtain demand ID.
                Also must be given a parameter to change like "elevator_id", "start_floor", "end_floor" 
                in dictionary format like this 
                "new_values":{
                    "end_floor": "new_value"
                    }'''
             }), 400
    
    return update_demand_controller(data)


@demand_blueprint.route('/delete', methods=['DELETE'])
def delete_demands():
    """
    Call this endpoint to delete an elevator in the DB.

    {
        "id": 2
    }
    """
    keys = ["id"]
    data = request.json

    if not all([key in data for key in keys]):
        return jsonify(
            {
                'error': '''demand ID is required for delete it from DB.
                 Please do a GET request to demand/get to obtain demand ID'''
             }), 400
    
    return delete_demand_controller(data)
