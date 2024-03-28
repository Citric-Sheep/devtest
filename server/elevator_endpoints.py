"""
Elevator endpoints
"""

from flask import Blueprint, jsonify, request
from controllers.elevator_controllers import *


elevator_blueprint = Blueprint('elevator', __name__)


# Endpoint for retrieving all elevators. Building ID parameter can be passed.
@elevator_blueprint.route('/get', defaults={'building_id': None}, methods=['GET'])
@elevator_blueprint.route('/get/<int:building_id>', methods=['GET'])
def get_elevators(building_id):
    """
    Call this endpoint when you want to retrieve an elevator entry in the DB.
    Building ID can be passed as query param. If not passed, it will return all elevators.
    """
    return get_elevators_controller(building_id)


@elevator_blueprint.route('/create', methods=['POST'])
def create_elevator():
    """
    Call this endpoint to create a new elevator in the DB. Building should be created previously so that building ID is 
    available to create the relationship.
    Expected body:

    {
        "max_floors": 2,
        "local_identifier":3
    }
    """
    data = request.json
    keys = ["building_id", "max_floors", "local_identifier"]

    if not all([key in data for key in keys]):
        return jsonify({'error': 'Building ID, max_floors and local_identifier are required'}), 400

    return create_elevator_controller(data)


@elevator_blueprint.route('/update', methods=['PUT'])
def update_elevators():
    """
    Call this endpoint to update an elevator in the DB.
    Expected body:

    {
        "id": 2,
        "new_values":
            {
                "local_identifier": 3
            }
    }

    So the elevator with ID 2 is going to be updated with the local identifier 3
    """
    keys = ["id", "new_values"]
    data = request.json

    if not all((key in data for key in keys)):
        return jsonify(
            {
                'error': '''elevator ID is required for updating it in DB.
                 Please do a GET request to "elevator/get" to obtain elevator ID.
                Also must be given a parameter to change like "building_id", "max_floors", "local_identifier" 
                in dictionary format like this:
                "new_values":{
                    "max_floors": "new_value"
                    }'''
             }), 400
    
    return update_elevator_controller(data)


@elevator_blueprint.route('/delete', methods=['DELETE'])
def delete_elevators():
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
                'error': '''elevator ID is required for delete it from DB. 
                Please do a GET request to elevator/get to obtain elevator ID'''
             }), 400
    
    return delete_elevator_controller(data)
