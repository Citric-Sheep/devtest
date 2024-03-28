"""
Building endpoints
"""

from flask import Blueprint, jsonify, request
from controllers.building_controllers import *


building_blueprint = Blueprint('building', __name__)


@building_blueprint.route('/get', defaults={'building_id': None}, methods=['GET'])
@building_blueprint.route('/get/<int:building_id>', methods=['GET'])
def get_buildings(building_id):
    """
    Call this endpoint when you want to retrieve a building entry in the DB.
    Building ID can be passed as query param. If not passed, it will return all buildings.
    """
    data = {"id": building_id} if building_id else None
    return get_buildings_controller(data)


@building_blueprint.route('/create', methods=['POST'])
def create_buildings():
    """
    Call this endpoint to create a new building in the DB.
    Expected body:

    {
        "name": "Junior II",
        "address": "Baez 619",
        "city": "Buenos Aires",
        "country": "Argentina"
    }
    """
    keys = ["name", "address", "city", "country"]
    data = request.json

    if not all([key in data for key in keys]):
        return jsonify({'error': 'Building name, address, city and country are required'}), 400
    
    return create_building_controller(data)


@building_blueprint.route('/update', methods=['PUT'])
def update_buildings():
    """
    Call this endpoint to update a building in the DB.
    Expected body:

    {
        "id": 2,
        "new_values":
            {
                "address": "Baez 619"
            }
    }

    So the elevator with ID 2 is going to be updated with the local identifier 3
    """
    keys = ["id", "new_values"]
    data = request.json

    if not all((key in data for key in keys)):
        return jsonify(
            {
                'error': '''Building ID is required for updating it in DB. Please do a GET request to building/get to obtain building ID.
                Also must be given a parameter to change like name, address, city or country in dictionary format like this 
                "new_values":{
                    "name": "new_value"
                    }'''
             }), 400
    
    return update_building_controller(data)


@building_blueprint.route('/delete', methods=['DELETE'])
def delete_buildings():
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
                'error': 'Building ID is required for delete it from DB. Please do a GET request to building/get to obtain building ID'
             }), 400
    
    return delete_building_controller(data)
